/* eslint-disable import/no-unresolved */
import useAutoCounter from '@hooks/useAutoCounter';

import Chart from 'react-apexcharts';
import getDefaultChartsColors from '@helpers/getDefaultChartsColors';

import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

import ChevronRightIcon from '@mui/icons-material/ChevronRight';

function GraphsSection({data}) {
	console.log('Graph Data:', data); // Debugging Line
	return (
		<section>
			<Grid container spacing={3} mt={1}>
				<Grid item xs={12} sm={12} md={12}>
					<Grid container spacing={3}>
						<Grid item xs={12} sm={4} md={4}>
							<ScannedTransaction data={data} />
						</Grid>
						<Grid item xs={12} sm={4} md={4}>
							<UnresolvedTransaction  data={data}/>
						</Grid>
						<Grid item xs={12} sm={4} md={4}>
							<ResolvedTransaction data={data} />
						</Grid>
					</Grid>
				</Grid>
				{/* <Grid item xs={12} sm={12} md={6}>
					<BitcoinEarningsSection />
				</Grid> */}
			</Grid>
		</section>
	);
}

function SectionContainer({ children, background }) {
	return (
		<Card
			sx={{
				position: 'relative',
				height: '100%',
			}}
			p={1}
		>
			<Box position="absolute" top="0" bottom="0" left="0" right="0" p={1}>
				{background}
			</Box>
			{children}
		</Card>
	);
}


const scannedTransactionConfig = {
	options: {
		colors: getDefaultChartsColors(2),
		chart: {
			toolbar: {
				show: false,
			},
			sparkline: {
				enabled: true,
			},
			parentHeightOffset: 0,
		},
		stroke: {
			curve: 'straight',
			width: 1,
		},
		markers: {
			size: 0,
		},
		grid: {
			show: false,
		},
		xaxis: {
			show: false,
		},
		tooltip: {
			enabled: false,
		},
		yaxis: {
			show: false,
		},
	},
	series: [
		{
			name: 'series-1',
			data: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
		},
	],
};

function ScannedTransaction({data}) {

	console.log('data.resolved_transactions,', data.scanned_transactions)
	const counter = useAutoCounter({
		limiter: data.scanned_transactions,
		increment: 1000,
		interval: 10,
	});
	return (
		<SectionContainer
			background={
				<Chart
					options={scannedTransactionConfig.options}
					series={scannedTransactionConfig.series}
					type="area"
					style={{
						position: 'absolute',
						bottom: '-10px',
						left: '-10px',
						right: '-10px',
					}}
					width="100%"
					height="13%"
				/>
			}
		>
			<Stack spacing={0} direction="column" width="100%" justifyContent="center" alignItems="center">
				<Typography variant="subtitle1" fontSize={35}>
					{counter.toLocaleString()}
				</Typography>
				<Typography variant="subtitle1">Scanned Transactions</Typography>
				<Typography variant="subtitle2" color="text.secondary" pb={2}>
				A scanned transaction refers to a payment record analyzed for patterns, risks, and anomalies using AI-driven monitoring tools like ReconX. 
				</Typography>
			</Stack>
		</SectionContainer>
	);
}

// Unresolved Transaction

const unresolvedTransactionConfig = {
	options: {
		colors: getDefaultChartsColors(4),
		chart: {
			toolbar: {
				show: false,
			},
			sparkline: {
				enabled: true,
			},
			parentHeightOffset: 0,
		},
		stroke: {
			curve: 'straight',
			width: 1,
		},
		markers: {
			size: 0,
		},
		grid: {
			show: false,
		},
		xaxis: {
			show: false,
		},
		tooltip: {
			enabled: false,
		},
		yaxis: {
			show: false,
		},
	},
	series: [
		{
			name: 'series-1',
			data: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
		},
	],
};
function UnresolvedTransaction({data}) {
	const counter = useAutoCounter({
		limiter: data.unresolved_transactions,
		increment: 1000,
		interval: 10,
	});
	return (
		<SectionContainer
			background={
				<Chart
					options={unresolvedTransactionConfig.options}
					series={unresolvedTransactionConfig.series}
					type="area"
					style={{
						position: 'absolute',
						bottom: '-10px',
						left: '-10px',
						right: '-10px',
					}}
					width="100%"
					height="13%"
				/>
			}
		>
			<Stack spacing={0} direction="column" width="100%" justifyContent="center" alignItems="center">
				<Typography variant="subtitle1" fontSize={35}>
					{counter.toLocaleString()}
				</Typography>
				<Typography variant="subtitle1">Unresolved Transactions</Typography>
				<Typography variant="subtitle2" color="text.secondary" pb={2}>
				An unresolved transaction refers to a financial transaction that has not yet been processed, analyzed, or verified by the system.
				</Typography>
			</Stack>
		</SectionContainer>
	);
}



const resolvedTransactionConfig = {
	options: {
		colors: getDefaultChartsColors(1),
		chart: {
			toolbar: {
				show: false,
			},
			sparkline: {
				enabled: true,
			},
			parentHeightOffset: 0,
		},
		stroke: {
			curve: 'straight',
			width: 1,
		},
		markers: {
			size: 0,
		},
		grid: {
			show: false,
		},
		xaxis: {
			show: false,
		},
		tooltip: {
			enabled: false,
		},
		yaxis: {
			show: false,
		},
	},
	series: [
		{
			name: 'series-1',
			data: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
		},
	],
};
function ResolvedTransaction({data}) {

	console.log('data.resolved_transactions,', data.resolved_transactions)
	const counter = useAutoCounter({
		limiter: data.resolved_transactions,
		increment: 1000,
		interval: 10,
	});
	return (
		<SectionContainer
			background={
				<Chart
					options={resolvedTransactionConfig.options}
					series={resolvedTransactionConfig.series}
					type="area"
					style={{
						position: 'absolute',
						bottom: '-10px',
						left: '-10px',
						right: '-10px',
					}}
					width="100%"
					height="13%"
				/>
			}
		>
			<Stack spacing={0} direction="column" width="100%" justifyContent="center" alignItems="center">
				<Typography variant="subtitle1" fontSize={35}>
					{counter.toLocaleString()}
				</Typography>
				<Typography variant="subtitle1">Resolved Transactions</Typography>
				<Typography variant="subtitle2" color="text.secondary" pb={2}>
				A resolved transaction refers to a previously disputed or flagged payment that has been successfully reviewed and addressed. 
				</Typography>
			</Stack>
		</SectionContainer>
	);
}



export default GraphsSection;
