# python3
import os
import binascii
import codecs
import grpc
from google.protobuf.json_format import MessageToJson
from python_lnd_grpc.lnd_defaults import defaultTLSCertFilename, defaultAdminMacFilename, defaultNetwork, defaultRPCHost, defaultRPCPort
import python_lnd_grpc.protos.rpc_pb2 as lnrpc
import python_lnd_grpc.protos.rpc_pb2_grpc as rpcstub
import python_lnd_grpc.protos.walletunlocker_pb2 as walletunlocker
import python_lnd_grpc.protos.walletunlocker_pb2_grpc as walletunlockerstub


# TODO: path for for system other than linux
TLS_FILE_PATH = '~/.lnd/'
ADMIN_MACAROON_PATH = '~/.lnd/data/chain/bitcoin/'


class Connector(object):
    def __init__(
        self,
        tls_file_path: str = TLS_FILE_PATH,
        tls_file_name: str = defaultTLSCertFilename,
        macaroon_path: str = ADMIN_MACAROON_PATH,
        macaroon_filename: str = defaultAdminMacFilename,
        network: str = defaultNetwork,
        grpc_host: str = defaultRPCHost,
        grpc_port: str = defaultRPCPort,
        custom_tls_path_full: str = None,
        custom_macaroon_path_full: str = None,
        output: str = None):

        # TODO move to separate method
        if custom_tls_path_full is not None:
            self.tls_file = os.path.expanduser(custom_tls_path_full)
        else:
            self.tls_file = os.path.expanduser(tls_file_path + tls_file_name)
        # print(self.tls_file)

        # TODO move to separate method
        if custom_macaroon_path_full is not None:
            self.full_macaroon_path = os.path.expanduser(custom_macaroon_path_full)
        else:
            self.full_macaroon_path = os.path.expanduser((macaroon_path + '{}/' + macaroon_filename).format(network))
        # print(self.full_macaroon_path)
        with open(self.tls_file, 'rb') as f:
            self.cert = f.read()
        with open(self.full_macaroon_path, 'rb') as f:
            self.macaroon_bytes = f.read()
            self.macaroon = codecs.encode(self.macaroon_bytes, 'hex')
        self.headers = {'Grpc-Metadata-macaroon': self.macaroon}
        self.host = grpc_host
        self.port = grpc_port
        self.output = output

    @property
    def _ln_stub(self):
        channel = grpc.secure_channel((self.host + ":" + self.port), self.combined_credentials)
        return rpcstub.LightningStub(channel)

    @property
    def _walletunlocker_stub(self):
        unlocker = grpc.secure_channel((self.host + ":" + self.port), self.ssl_credentials())
        return walletunlockerstub.WalletUnlockerStub(unlocker)

    @property
    def combined_credentials(self) -> grpc.CallCredentials:
        ssl_creds = grpc.ssl_channel_credentials(self.cert)
        auth_creds = grpc.metadata_call_credentials(self.auth_metadata_plugin)
        return grpc.composite_channel_credentials(ssl_creds, auth_creds)

    def ssl_credentials(self):
        ssl_creds = grpc.ssl_channel_credentials(self.cert)
        return ssl_creds

    def auth_metadata_plugin(self, _, callback):
        callback([("macaroon", self.macaroon)], None)

    def out(self, response):
        if self.output == "json":
            return MessageToJson(response)
        elif self.output == "json-none-included":
            return MessageToJson(response, including_default_value_fields=True)
        else:
            return response


class WalletUnlocker(Connector):
    # https://api.lightning.community/#changepassword
    def changepassword(self, current_password: bytes, new_password: bytes):
        request = walletunlocker.ChangePasswordRequest(
            current_password=current_password,
            new_password=new_password,
        )
        response = self._walletunlocker_stub.ChangePassword(request)
        return response

    # https://api.lightning.community/#genseed
    def genseed(self, aezeed_passphrase: bytes, seed_entropy: bytes):
        request = walletunlocker.GenSeedRequest(
            aezeed_passphrase=aezeed_passphrase,
            seed_entropy=seed_entropy,
        )
        response = self._walletunlocker_stub.GenSeed(request)
        return response

    # https://api.lightning.community/#initwallet
    def initwallet(
        self, 
        wallet_password: bytes,
        cipher_seed_mnemonic,
        aezeed_passphrase: bytes,
        recovery_window: int,
        channel_backups):
        request = walletunlocker.InitWalletRequest(
            wallet_password=wallet_password,
            cipher_seed_mnemonic=cipher_seed_mnemonic,
            aezeed_passphrase=aezeed_passphrase,
            recovery_window=recovery_window,
            channel_backups=channel_backups,
        )
        response = self._walletunlocker_stub.InitWallet(request)
        return response

    # https://api.lightning.community/#unlockwallet
    def unlockwallet(self, wallet_password: bytes, recovery_window: int, channel_backups):
        request = walletunlocker.UnlockWalletRequest(
            wallet_password=wallet_password,
            recovery_window=recovery_window,
            channel_backups=channel_backups,
        )
        response = self._walletunlocker_stub.UnlockWallet(request)
        return response


class LNDMethods(Connector):
    # https://api.lightning.community/#abandonchannel
    def abandonchannel(self, channel_point):
        request = lnrpc.AbandonChannelRequest(
            channel_point = channel_point,
        )
        response = self._ln_stub.AbandonChannel(request)
        return self.out(response)

    # https://api.lightning.community/#closechannel
    def closechannel(self, channel_point, force: bool, target_conf: int, sat_per_byte: int, delivery_address: str):
        request = lnrpc.CloseChannelRequest(
            channel_point=channel_point,
            force=force,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            delivery_address=delivery_address,
        )
        response = self._ln_stub.CloseChannel(request)
        return self.out(response)

    # https://api.lightning.community/#channelbalance
    def channelbalance(self):
        response = self._ln_stub.ChannelBalance(lnrpc.ChannelBalanceRequest())
        return self.out(response)
    
    # https://api.lightning.community/#connectpeer
    def connectpeer(self, pubkey: str, host: str, perm: bool = False):
        #async when perm = True
        address = lnrpc.LightningAddress(pubkey=pubkey, host=host)
        request = lnrpc.ConnectPeerRequest(addr = address, perm = perm)
        response = self._ln_stub.ConnectPeer(request)
        return self.out(response)

    # https://api.lightning.community/#decodepayreq
    def decode_pay_req(self, pub_key: str):
        request = lnrpc.PayReqString(
            pub_key=pub_key,
        )
        response = self._ln_stub.DecodePayReq(request)
        return self.out(response)

    # https://api.lightning.community/#describegraph
    def describegraph(self, include_unannounced: bool):
        # TODO define specific variables for big message channel, format length of the line
        channel = grpc.secure_channel((self.host + ":" + self.port), grpc.ssl_channel_credentials(self.cert), options=[('grpc.max_send_message_length', 20000000), ('grpc.max_receive_message_length', 20000000)])
        stub = rpcstub.LightningStub(channel)
        request = lnrpc.ChannelGraphRequest(
            include_unannounced=include_unannounced,
        )
        response = stub.DescribeGraph(request, metadata=[('macaroon', self.macaroon)])
        return self.out(response)

    # https://api.lightning.community/#disconnectpeer
    def disconnect(self, pub_key: str):
        request = lnrpc.DisconnectPeerRequest(
            pub_key=pub_key,
        )
        response = self._ln_stub.DisconnectPeer(request)
        return self.out(response)

    # https://api.lightning.community/#estimatefee
    def estimatefee(self, addr_to_amount, target_conf: int):
        request = lnrpc.EstimateFeeRequest(
            AddrToAmount=addr_to_amount,
            target_conf=target_conf,
        )
        response = self._ln_stub.EstimateFee(request)
        return self.out(response)

    # https://api.lightning.community/#feereport
    def feereport(self):
        response = self._ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return self.out(response)

     # https://api.lightning.community/#getchaninfo
    def getchaninfo(self, chan_id: int):
        request = lnrpc.ChanInfoRequest(
            chan_id=chan_id,
        )
        response = self._ln_stub.GetChanInfo(request)
        return self.out(response)

    # https://api.lightning.community/#getinfo
    def getinfo(self):
        response = self._ln_stub.GetInfo(lnrpc.GetInfoRequest())
        return self.out(response)

    # https://api.lightning.community/#getnetworkinfo
    def getnetworkinfo(self):
        response = self._ln_stub.GetNetworkInfo(lnrpc.NetworkInfoRequest())
        return self.out(response)

    # https://api.lightning.community/#getnodeinfo
    def getnodeinfo(self, pub_key: str, include_channels: bool):
        request = lnrpc.NodeInfoRequest(
            pub_key=pub_key,
            include_channels=include_channels,
        )
        response = self._ln_stub.GetNodeInfo(request)
        return self.out(response)

    # https://api.lightning.community/#getrecoveryinfo
    def getrecoveryinfo(self):
        response = self._ln_stub.GetRecoveryInfo(lnrpc.GetRecoveryInfoRequest())
        return self.out(response)

    # https://api.lightning.community/#gettransactions
    def gettransactions(self, start_height: int, end_height: int):
        request = lnrpc.GetTransactionsRequest(
            start_height=start_height,
            end_height=end_height,
        )
        response = self._ln_stub.GetTransactions(request)
        return self.out(response)

    # https://api.lightning.community/#listchannels
    def listchannels(
        self, 
        active_only: bool = None, 
        inactive_only: bool = None, 
        public_only: bool = None,
        private_only: bool = None, 
        peer: bytes = None):
        request = lnrpc.ListChannelsRequest(
            active_only=active_only,
            inactive_only=inactive_only,
            public_only=public_only,
            private_only=private_only,
            peer=peer,
        )
        response = self._ln_stub.ListChannels(request)
        return self.out(response)

    # https://api.lightning.community/#listinvoices
    def listinvoices(self, pending_only: bool, index_offset: int, num_max_invoices: int, reverse: bool):
        request = lnrpc.ListInvoiceRequest(
            pending_only=pending_only,
            index_offset=index_offset,
            num_max_invoices=num_max_invoices,
            reversed=reverse,
        )
        response = self._ln_stub.ListInvoices(request)
        return self.out(response)

    # https://api.lightning.community/#listpayments
    def listpayments(self, include_incomplete: bool, index_offset: int, max_payments: int, reverse: bool):
        request = lnrpc.ListPaymentsRequest(
            include_incomplete=include_incomplete,
            index_offset=index_offset,
            max_payments=max_payments,
            reversed=reverse,
        )
        response = self._ln_stub.ListPayments(request)
        return self.out(response)

    # https://api.lightning.community/#listpeers
    def listpeers(self, latest_error: bool = None):
        request = lnrpc.ListPeersRequest(
            latest_error=latest_error,
        )
        response = self._ln_stub.ListPeers(request)
        return self.out(response)

    # https://api.lightning.community/#listunspent
    def listunspent(self, min_confs: int, max_confs: int):
        request = lnrpc.ListUnspentRequest(
            min_confs=min_confs,
            max_confs=max_confs,
        )
        response = self.stub.ListUnspent(request)
        return self.out(response)

    # https://api.lightning.community/#lookupinvoice
    def lookupinvoice(self, r_hash_str: str, r_hash: bool):
        request = lnrpc.PaymentHash(
            r_hash_str=r_hash_str,
            r_hash=r_hash,
        )
        response = self._ln_stub.LookupInvoice(request)
        return self.out(response)

    # https://api.lightning.community/#newaddress
    def newaddress(self):
        response = self._ln_stub.NewAddress(lnrpc.NewAddressRequest())
        return self.out(response)

    # https://api.lightning.community/#openchannel
    def openchannel(
        self, 
        node_pubkey: bytes,
        node_pubkey_string: str,
        local_funding_amount: int,
        push_sat: int,
        target_conf: int,
        sat_per_byte: int,
        private: bool,
        min_htlc_msat: int,
        remote_csv_delay: int,
        min_confs: int,
        spend_unconfirmed: bool,
        close_address: str,
        fundingShim,
        remote_max_value_in_flight_msat: int):
        request = lnrpc.OpenChannelRequest(
            node_pubkey=node_pubkey,
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=local_funding_amount,
            push_sat=push_sat,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            private=private,
            min_htlc_msat=min_htlc_msat,
            remote_csv_delay=remote_csv_delay,
            min_confs=min_confs,
            spend_unconfirmed=spend_unconfirmed,
            close_address=close_address,
            funding_shim=funding_shim,
            remote_max_value_in_flight_msat=remote_max_value_in_flight_msat,
        )
        response = self._ln_stub.OpenChannel(request)
        return self.out(response)

    # https://api.lightning.community/#openchannelsync
    def openchannelsync(
        self, 
        node_pubkey: bytes,
        node_pubkey_string: str,
        local_funding_amount: int,
        push_sat: int,
        target_conf: int,
        sat_per_byte: int,
        private: bool,
        min_htlc_msat: int,
        remote_csv_delay: int,
        min_confs: int,
        spend_unconfirmed: bool,
        close_address: str,
        fundingShim,
        remote_max_value_in_flight_msat: int):
        request = lnrpc.OpenChannelRequest(
            node_pubkey=node_pubkey,
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=local_funding_amount,
            push_sat=push_sat,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            private=private,
            min_htlc_msat=min_htlc_msat,
            remote_csv_delay=remote_csv_delay,
            min_confs=min_confs,
            spend_unconfirmed=spend_unconfirmed,
            close_address=close_address,
            funding_shim=funding_shim,
            remote_max_value_in_flight_msat=remote_max_value_in_flight_msat,
        )
        response = self._ln_stub.OpenChannelSync(request)
        return self.out(response)

    # https://api.lightning.community/#pendingchannels
    def pendingchannels(self):
        response = self._ln_stub.PendingChannels(lnrpc.PendingChannelsRequest())
        return self.out(response)

    # https://api.lightning.community/#restorechannelbackups
    def restorechanbackup(self, chan_backups, multi_chan_backup: bytes):
        request = lnrpc.RestoreChanBackupRequest(
            chan_backups=chan_backups,
            multi_chan_backup=multi_chan_backup,
        )
        response = self._ln_stub.RestoreChannelBackups(request)
        return self.out(response)

    # https://api.lightning.community/#sendcoins
    def sendcoins(self, addr: str, amount: int, target_conf: int, sat_per_byte: int, send_all: bool, label: str):
        request = lnrpc.SendCoinsRequest(
            addr=addr,
            amount=amount,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            send_all=send_all,
            label=label,
        )
        response = self._ln_stub.SendCoins(request)
        return self.out(response)

    # https://api.lightning.community/#sendmany
    def sendmany(self, AddrToAmount, target_conf: int, sat_per_byte: int, label: str):
        request = lnrpc.SendManyRequest(
            AddrToAmount=AddrToAmount,
            target_conf=target_conf,
            sat_per_byte=sat_per_byte,
            label=label,
        )
        response = self._ln_stub.SendMany(request)
        return self.out(response)

    # https://api.lightning.community/#sendpaymentsync
    def sendpaymentssync(
        self,
        dest: bytes,
        dest_string: str,
        amt: int,
        amt_msat: int,
        pament_hash: bytes,
        payment_hash_string: str,
        payment_request: str,
        final_cltv_delta: int,
        fee_limit,
        outgoing_chan_id: int,
        last_hop_pubkey: bytes,
        cltv_limit: int,
        dest_custom_records,
        allow_self_payment: bool,
        dest_features):
        request = lnrpc.SendRequest(
            dest=dest,
            dest_string=dest_string,
            amt=amt,
            amt_msat=amt_msat,
            payment_hash=payment_hash,
            payment_hash_string=payment_hash_string,
            payment_request=payment_request,
            final_cltv_delta=final_cltv_delta,
            fee_limit=fee_limit,
            outgoing_chan_id=outgoing_chan_id,
            last_hop_pubkey=last_hop_pubkey,
            cltv_limit=cltv_limit,
            dest_custom_records=dest_custom_records,
            allow_self_payment=allow_self_payment,
            dest_features=dest_features,
        )
        response = self._ln_stub.SendPaymentSync(request)
        return self.out(response)

    def sendtoroute(self, payment_hash: bytes, payment_hash_string: str, route):
        request = lnrpc.SendToRouteRequest(
            payment_hash=payment_hash,
            payment_hash_string=payment_hash_string,
            route=route,
        )
        response = self._ln_stub.SendToRouteSync(request)
        return self.out(response)

    def subscribechannelbackups(self):
        response = self._ln_stub.SubscribeChannelBackups(lnrpc.ChannelBackupSubscription())
        return self.out(response)

    

    # https://api.lightning.community/#walletbalance
    def walletbalance(self):
        response = self._ln_stub.WalletBalance(lnrpc.WalletBalanceRequest()) 
        return self.out(response)

    '''
    def forwarding_history(self):
        request = lnrpc.ForwardingHistoryRequest(
        start_time=<uint64>,
        end_time=<uint64>,
        index_offset=<uint32>,
        num_max_events=<uint32>,
        )
        response = self.ln_stub.FeeReport(lnrpc.FeeReportRequest())
        return response
    '''