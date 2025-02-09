const apiconfig = {
    summarydata: "http://192.168.82.193:8000/transaction_stats",
    dashboardtabledata: "http://192.168.82.193:8000/reconcile_data",
    dashboardModalBarchart: "http://192.168.82.193:8000/discrepancy_categories",
    dashboardreportdata: "http://192.168.82.193:8000/discrepancy_cases",
    dashboardAnalysis:"http://192.168.82.193:8000/reconciliation_summaries",

    // payment methods
    getPaymentMethodUrl: "http://192.168.82.193:8000/fetch_three_tables",
    getPayment4MethodUrl: "http://192.168.82.193:8000/fetch_four_tables",
    uploadCsvUrl: "http://192.168.82.193:8000/upload_csv",
    consolidatedtable: "http://192.168.82.193:8000/fetch_consolidated_table",

  };
  
  export default apiconfig;
  