import structlog
from eth_utils import decode_hex, is_binary_address, to_canonical_address

from raiden.network.rpc.client import JSONRPCClient, check_address_has_code
from raiden.utils.typing import Address, BlockSpecification, OneToNAddress, TokenAddress
from raiden_contracts.constants import CONTRACT_ONE_TO_N
from raiden_contracts.contract_manager import ContractManager

log = structlog.get_logger(__name__)


class OneToN:
    def __init__(
        self,
        jsonrpc_client: JSONRPCClient,
        one_to_n_address: OneToNAddress,
        contract_manager: ContractManager,
    ):
        if not is_binary_address(one_to_n_address):
            raise ValueError("Expected binary address for monitoring service")

        self.contract_manager = contract_manager
        check_address_has_code(
            client=jsonrpc_client,
            address=Address(one_to_n_address),
            contract_name=CONTRACT_ONE_TO_N,
            expected_code=decode_hex(
                contract_manager.get_runtime_hexcode(CONTRACT_ONE_TO_N)
            ),
        )

        proxy = jsonrpc_client.new_contract_proxy(
            abi=self.contract_manager.get_contract_abi(CONTRACT_ONE_TO_N),
            contract_address=Address(one_to_n_address),
        )

        self.address = one_to_n_address
        self.proxy = proxy
        self.client = jsonrpc_client
        self.node_address = self.client.address
