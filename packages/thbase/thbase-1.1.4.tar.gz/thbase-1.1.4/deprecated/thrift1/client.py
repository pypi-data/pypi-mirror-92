from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import Mutation
from thriftClientAPI import ClientBase


class Client(ClientBase):

    def __init__(self, host, port, info_port):
        super(Client, self).__init__(host, port, info_port)
        self.client = Hbase.Client(self.protocol)

    def put_row(self, table_name, row_key, families, qualifier, value):
        mutation_list = []
        for cf in families:
            mutation = Mutation(column=cf + ":" + qualifier, value=value)
            mutation_list.append(mutation)
        self.client.mutateRow(
            table_name, row_key, mutation_list, None
        )

    def get_row(self, table_name, row_key):
        result_list = self.client.getRow(table_name, row_key, None)
        final_dict = {}
        for result in result_list:
            row = result.row
            column_dict = {}
            for col in result.columns:
                column_dict[col] = result.columns[col].value
            final_dict[row] = column_dict
        return final_dict

    def scan(self, table_name, start_row_key, num_rows):
        scanner_id = self.client.scannerOpen(tableName=table_name,
                                             startRow=start_row_key,
                                             columns=None,
                                             attributes=None)
        result_list = self.client.scannerGetList(scanner_id, num_rows)
        self.client.scannerClose(scanner_id)
        final_dict = {}
        for result in result_list:
            row = result.row
            column_dict = {}
            for col in result.columns:
                column_dict[col] = result.columns[col].value
            final_dict[row] = column_dict
        return final_dict

    def delete_row(self, table_name, row_key):
        try:
            self.client.deleteAllRow(tableName=table_name, row=row_key, attributes=None)
            return True
        except:
            return False


class HttpClient(Client):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.transport = THttpClient.THttpClient("http://" + host + ":" + str(port))
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)

    def delete_row(self, table_name, row_key):
        self.client.deleteAllRow(table_name, row_key, None)
