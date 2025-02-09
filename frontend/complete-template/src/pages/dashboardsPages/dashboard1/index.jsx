/* eslint-disable import/no-unresolved */
/* eslint-disable import/extensions */
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
// import WelcomeSection from './welcomeSection';
import GraphsSection from './graphsSection';
import BitcoinSection from './bitcoinSection';
import BarChartSection from './barChart';
import Box from '@mui/material/Box';
import TransactionsSection from './transactionsSection';
import useApiCall from '../../../hooks/useApiCall';
import apiconfig from "../../../apiconfig/config.dev";
import {
	LogoLoader
} from '@/components/loader';
import Typography from '@mui/material/Typography';

function Dashboard1Page() {

	const apiUrlsummarydata = apiconfig.summarydata || {};
	const apiUrldashboardtabledata = apiconfig.dashboardtabledata || {};
	const apiUrlbarchartdata = apiconfig.dashboardModalBarchart || {};
	const apiUrldashboardreportdata = apiconfig.dashboardreportdata || {};
	const apiUrldashboardAnalysis = apiconfig.dashboardAnalysis || {};

	const { data: summarydata, loadingData: loadingSummary } = useApiCall(apiUrlsummarydata);
	const { data: dashboardtabledata, loadingData: loadingTable } = useApiCall(apiUrldashboardtabledata);
	const { data: barchartdata, loadingData: loadingBarChart } = useApiCall(apiUrlbarchartdata);
	const { data: dashboardreportdata, loadingData: loadingReport } = useApiCall(apiUrldashboardreportdata);
	const { data: dashboardAnalysis, loadingData: loadingAnalysis } = useApiCall(apiUrldashboardAnalysis);
	
	const isLoading = loadingSummary || loadingTable || loadingBarChart || loadingReport || loadingAnalysis;

	if (isLoading) {
        return <Box display="flex" minHeight="100vh" flexDirection="column"><LogoLoader mt={3}/></Box>; // Or use a skeleton UI component
    }
	
	return (
		<>
		
			<section>
				<Stack spacing={3}  mb={2}>
					<GraphsSection data={summarydata} />
				</Stack>
			</section>
			<section>
				<Grid container spacing={3} mb={2}>
					<Grid item xs={12} md={12} lg={6}>
						<BarChartSection data={barchartdata} />
					</Grid>

					<Grid item xs={12} md={12} lg={6}>
						<BitcoinSection data={dashboardreportdata} />
					</Grid>
				</Grid>
				<Grid container spacing={3} mb={3}>
					<Grid item xs={12} md={12} lg={12}>
						<TransactionsSection data={dashboardtabledata} />
					</Grid>
				</Grid>
			</section>

			<Grid container spacing={3} mb={3} mt={2}>
					<Grid item xs={12} md={12} lg={12}>
						<Typography variant="h5"  gutterBottom> Analysis: <Typography variant="subtitle2" style={{ color: 'black'}}  gutterBottom>{ dashboardAnalysis.summary || '' }</Typography></Typography>
						
				</Grid>
			</Grid>
			

		</>
	);
}

export default Dashboard1Page;
