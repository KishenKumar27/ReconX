
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import LinearProgress from '@mui/material/LinearProgress';

function BitcoinSection({data}) {
	return (
		<section>
			<Grid container spacing={3} >
				<Grid item xs={12} sm={12} md={12}>
					<Stack direction="column" spacing={3}>
						<SalesCard pt={2} pb={2} reportData={data} />
						{/* <ImpressionsCard /> */}
					</Stack>
				</Grid>
			</Grid>
		</section>
	);
}
const SALES_DATA = [
	{
		id: 1,
		type: 'Today',
		total: '1,898',
	},
	{
		id: 2,
		type: 'This Week',
		total: '32,112',
	},
	{
		id: 4,
		type: 'This Month',
		total: '72,067',
	},
];
function SalesCard({reportData}) {
	return (
		<Card
			sx={{
				height: '50%',
			}}
		>
			<Stack direction="column" spacing={1} justifyContent="center">
				<Typography color="primary.main" variant="h5" textTransform="uppercase">
					Report
				</Typography>
				<Stack
					width="100%"
					direction="row"
					divider={<Divider orientation="vertical" flexItem />}
					spacing={2}
					justifyContent="space-between"
					pb={3}
				>
					{reportData.map(({ id, type, total }) => (
						<div key={id}>
							<Typography variant="subtitle2" gutterBottom>
								{type}
							</Typography>
							<Typography variant="subtitle1" component="div">
								{total}
							</Typography>
						</div>
					))}
				</Stack>

				<Box
					sx={{
						width: '100%',
						position: 'relative',
					}}
				>
					<LinearProgress
						variant="determinate"
						value={50}
						sx={{
							height: 15,
						}}
					/>
					<Box
						sx={{
							width: '50%',
							top: 0,
							left: 0,
							bottom: 0,
							right: 0,
							position: 'absolute',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
						}}
					>
						<Typography variant="caption" component="div" color="primary.contrastText">
							{/* {`${Math.round(50)}%`} */}
						</Typography>
					</Box>
				</Box>
				<Typography color="text.secondary" align='center'>Overall analysis report</Typography>
			</Stack>
		</Card>
	);
}

// const impressionsGraphConfig = {
// 	options: {
// 		colors: getDefaultChartsColors(3),
// 		chart: {
// 			toolbar: {
// 				show: false,
// 			},
// 			sparkline: {
// 				enabled: true,
// 			},
// 			parentHeightOffset: 0,
// 		},
// 		stroke: {
// 			width: 2,
// 		},
// 		markers: {
// 			size: 0,
// 		},
// 		grid: {
// 			show: false,
// 		},
// 		xaxis: {
// 			show: false,
// 		},
// 		tooltip: {
// 			enabled: false,
// 		},
// 		yaxis: {
// 			show: false,
// 		},
// 	},
// 	series: [
// 		{
// 			name: 'series-1',
// 			data: [9, 13, 12, 15, 12, 11, 15, 16, 17, 10, 15],
// 		},
// 	],
// };
// function ImpressionsCard() {
// 	return (
// 		<Card
// 			sx={{
// 				position: 'relative',
// 				height: '50%',
// 			}}
// 		>
// 			<Stack direction="column" spacing={1} pb={6}>
// 				<Typography color="primary.main" variant="h5" textTransform="uppercase">
// 					Impressions
// 				</Typography>
// 				<Typography variant="body2" fontSize={27}>
// 					323,360
// 				</Typography>
// 				<Stack direction="row" alignItems="center" spacing={0.5}>
// 					<Avatar
// 						sx={{
// 							bgcolor: 'success.light',
// 							color: 'success.dark',
// 							width: 24,
// 							height: 24,
// 						}}
// 						variant="rounded"
// 					>
// 						<ArrowUpwardIcon fontSize="small" />
// 					</Avatar>
// 					<Typography color="success.main" component="span" ml={1}>
// 						2.5%
// 					</Typography>
// 					<Typography variant="body1" color="text.secondary">
// 						change from yesterday
// 					</Typography>
// 				</Stack>
// 			</Stack>
// 			<Box position="absolute" top="0" bottom="0" left="0" right="0">
// 				<Chart
// 					options={impressionsGraphConfig.options}
// 					series={impressionsGraphConfig.series}
// 					type="area"
// 					style={{
// 						position: 'absolute',
// 						bottom: 0,
// 						left: 0,
// 						right: 0,
// 					}}
// 					width="100%"
// 					height="40%"
// 				/>
// 			</Box>
// 		</Card>
// 	);
// }

export default BitcoinSection;
