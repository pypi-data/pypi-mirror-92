import logging
from ordered_set import OrderedSet

from crosspm.contracts.package import is_packages_contracts_graph_resolvable
from crosspm.helpers.exceptions import CrosspmException, CROSSPM_ERRORCODE_PACKAGE_NOT_FOUND, \
    CrosspmBundleNoValidContractsGraph, CrosspmBundleTriggerPackagesHasNoValidContractsGraph


class Bundle:
    def __init__(self, deps, packages_repo, trigger_packages):
        # it is vital for deps to be list, orderedset (or something with insertion order savings),
        # we need the order of packages in dependencies.txt to take next package
        # when no contracts satisfied
        self._log = logging.getLogger('crosspm')

        self._deps = OrderedSet(deps)
        self._packages_repo = sorted(packages_repo, reverse=True)

        self._trigger_packages = []
        if trigger_packages:
            for tp in trigger_packages:
                self._trigger_packages.append(Bundle.find_trigger_package_in_packages_repo(tp, self._packages_repo))

        self._packages = dict()
        self._bundle_contracts = {}

    @staticmethod
    def find_trigger_package_in_packages_repo(trigger_package, repo_packages):

        for p in repo_packages:
            if p == trigger_package:
                return p

        raise CrosspmException(CROSSPM_ERRORCODE_PACKAGE_NOT_FOUND,
                               f"trigger_package = <{trigger_package}> NOT FOUND in repo_packages : {repo_packages}")

    def calculate(self):

        self._log.info('deps: {}'.format(self._deps))
        self._log.info('trigger_packages: {}'.format(self._trigger_packages))
        self._log.info('packages_repo: {}'.format(self._packages_repo))

        if not is_packages_contracts_graph_resolvable(self._trigger_packages):
            raise CrosspmBundleTriggerPackagesHasNoValidContractsGraph(self._trigger_packages)

        for tp in self._trigger_packages:
            self._packages[tp.name] = tp

        while True:
            rest_packages_to_find = self.rest_packages_to_find(self._deps, self._packages)
            if not rest_packages_to_find:
                break

            self.update_bundle_contracts()
            self.find_next_microservice_package(rest_packages_to_find)

        return self._packages

    def find_next_microservice_package(self, rest_packages_to_find):
        next_packages_out_of_current_contracts = dict()
        package_lowering_contract = []

        for m in rest_packages_to_find:
            for p in [i for i in self._packages_repo if i.is_microservice(m)]:
                package = self.is_package_corresponds_bundle_current_contracts(next_packages_out_of_current_contracts,
                                                                               p,
                                                                               self._bundle_contracts,
                                                                               package_lowering_contract)
                if package:
                    self._package_add(package)
                    return

            if package_lowering_contract:
                p = package_lowering_contract[0]

                self.remove_packages_with_higher_contracts_then(p)
                self._package_add(p)

                return

        package = self.select_next_microservice_package_out_of_current_contracts(next_packages_out_of_current_contracts,
                                                                                 rest_packages_to_find)
        if package:
            self._package_add(package)
            return

        raise CrosspmBundleNoValidContractsGraph(f"cant select next package for current contracts:\n"
                                                 f"next_packages_out_of_current_contracts : {next_packages_out_of_current_contracts}\n"
                                                 f"rest_packages_to_find : {rest_packages_to_find}\n"
                                                 f"bundle.packages : {self._packages}")

    def select_next_microservice_package_out_of_current_contracts(self, next_packages_out_of_current_contracts,
                                                                  select_order):
        for i in select_order:
            if i in next_packages_out_of_current_contracts:
                return next_packages_out_of_current_contracts[i]

        return None

    def is_package_corresponds_bundle_current_contracts(self, next_packages_out_of_current_contracts, package,
                                                        bundle_contracts, package_lowering_contract):

        intersection_package_contracts = package.calc_contracts_intersection(bundle_contracts)

        if not intersection_package_contracts:
            cp = None
            if package.name in next_packages_out_of_current_contracts:
                cp = next_packages_out_of_current_contracts[package.name]

            if cp is None:
                next_packages_out_of_current_contracts[package.name] = package
            elif cp.version < package.version:
                next_packages_out_of_current_contracts[package.name] = package

            return None

        failed_contracts = set(intersection_package_contracts)
        for c in intersection_package_contracts:

            if package.contracts[c] == bundle_contracts[c]:
                failed_contracts.discard(c)

            if package.contracts[c].value < bundle_contracts[c].value:
                if not package_lowering_contract:
                    package_lowering_contract.append(package)
                elif package_lowering_contract[0].is_contract_lower_then(package.contracts[c]):
                    package_lowering_contract.clear()
                    package_lowering_contract.append(package)

        if not failed_contracts:
            return package

    def remove_packages_with_higher_contracts_then(self, package_lowering_contract):

        for p in [*self._packages.values()]:
            if p.is_any_contract_higher(package_lowering_contract):
                if p in self._trigger_packages:
                    raise CrosspmBundleNoValidContractsGraph(
                        f"no tree resolve with trigger_packages {self._trigger_packages}, threre is no appropriate packages with specified package contracts")

                del self._packages[p.name]

    def update_bundle_contracts(self):
        self._bundle_contracts = dict()
        for p in self._packages.values():
            self._bundle_contracts.update(p.contracts)

    def rest_packages_to_find(self, deps, packages):
        return deps - packages.keys()

    def _package_add(self, package):
        self._packages[package.name] = package
