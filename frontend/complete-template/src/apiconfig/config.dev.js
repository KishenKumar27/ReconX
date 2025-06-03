const apiconfig = {
    summarydata: "http://localhost:8000/transaction_stats",
    dashboardtabledata: "http://localhost:8000/reconcile_data",
    dashboardModalBarchart: "http://localhost:8000/discrepancy_categories",
    dashboardreportdata: "http://localhost:8000/discrepancy_cases",
    dashboardAnalysis:"http://localhost:8000/reconciliation_summaries",

    // payment methods
    getPaymentMethodUrl: "http://localhost:8000/fetch_three_tables",
    getPayment4MethodUrl: "http://localhost:8000/fetch_four_tables",
    uploadCsvUrl: "http://localhost:8000/upload_csv",
    consolidatedtable: "http://localhost:8000/fetch_consolidated_table",

  };
  
  export default apiconfig;
