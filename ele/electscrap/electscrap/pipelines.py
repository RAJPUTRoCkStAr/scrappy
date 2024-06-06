import pandas as pd
from electscrap.items import ElectionResultItem, DetailedResultItem,ResdataItem,ThirddataItem

class ElectionPipeline:

    def open_spider(self, spider):
        self.election_results = []
        self.detailed_results = []
        self.resdata_results = []
        self.respdata_results = []

    def close_spider(self, spider):
        election_df = pd.DataFrame(self.election_results)
        detailed_df = pd.DataFrame(self.detailed_results)
        resdata_df = pd.DataFrame(self.resdata_results)
        respdata_df = pd.DataFrame(self.respdata_results)
        
        with pd.ExcelWriter('election_resulted.xlsx') as writer:
            election_df.to_excel(writer, sheet_name='Summary Results', index=False)
            detailed_df.to_excel(writer, sheet_name='Detailed Results', index=False)
            resdata_df.to_excel(writer, sheet_name='Resdata Results', index=False)
            respdata_df.to_excel(writer, sheet_name='Respdata Results', index=False)

    def process_item(self, item, spider):
        if isinstance(item, ElectionResultItem):
            self.election_results.append(dict(item))
        elif isinstance(item, DetailedResultItem):
            self.detailed_results.append(dict(item))
        elif isinstance(item, ResdataItem):
            self.resdata_results.append(dict(item))
        elif isinstance(item, ThirddataItem):
            self.respdata_results.append(dict(item))
        return item
