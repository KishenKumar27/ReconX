/* eslint-disable import/no-unresolved */
import { useState } from 'react';
import useAutoCounter from '@hooks/useAutoCounter';
import Chart from 'react-apexcharts';
import getDefaultChartsColors from '@helpers/getDefaultChartsColors';
import { useNavigate, Link as RouterLink } from 'react-router-dom';

import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import ModalBarChart from './modalChart';
import Avatar from '@mui/material/Avatar';

import ChevronRightIcon from '@mui/icons-material/ChevronRight';

function BarChartSection({ data }) {
	return (
		<section>
			<Grid container spacing={3} mb={1}>
				<Grid item xs={12}>
					<EtereumWalletSection data={data} />
				</Grid>
			</Grid>
		</section>
	);
}

function SectionContainer({ children, background }) {
	return (
		<Card sx={{ position: 'relative', height: '100%' }}>
			<Box position="absolute" top="0" bottom="0" left="0" right="0">
				{background}
			</Box>
			{children}
		</Card>
	);
}

const ethereumGraphConfig = {
	options: {
		colors: getDefaultChartsColors(1),
		plotOptions: {
			bar: { columnWidth: '95%' },
		},
		chart: {
			toolbar: { show: false },
			sparkline: { enabled: true },
			parentHeightOffset: 0,
		},
		grid: { show: false },
		xaxis: { show: false, categories: [1] },
		tooltip: { enabled: false },
		yaxis: { show: false },
	},
	series: [
		{ name: 'series-1', data: [20, 25, 10, 20, 15, 18, 15, 3, 2, 5, 3, 2, 4, 5, 1, 2] },
		{ name: 'series-2', data: [10, 30, 45, 30, 25, 15, 10, 4, 3, 2, 5, 2, 3, 2, 4, 5] },
	],
};

function EtereumWalletSection({ data }) {
	const [openModal, setOpenModal] = useState(false);

	const handleOpenModal = () => setOpenModal(true);
	const handleCloseModal = () => setOpenModal(false); 

	const counter = useAutoCounter({
		limiter: 0.0873,
		increment: 0.001,
		interval: 10,
	});

	return (
		<SectionContainer
			mb={2}
			background={
				<Chart
					options={ethereumGraphConfig.options}
					series={ethereumGraphConfig.series}
					type="bar"
					style={{ position: 'absolute', bottom: '0', left: '0', right: '0' }}
					width="100%"
					height="100%"
				/>
			}
		>
			<Stack ml="auto" width="50%" spacing={1}>
				<Typography variant="subtitle1" fontSize={16}>
					Mismatch Transactions
				</Typography>
				<Typography variant="subtitle2">
					A mismatch transaction refers to a payment that was initiated but not recorded or reconciled in the system.
				</Typography>
				<Button
					variant="text"
					size="small"
					endIcon={<ChevronRightIcon />}
					sx={{
						width: 'fit-content',
						textTransform: 'uppercase',
						backgroundColor: '#ececece',
					}}
					onClick={handleOpenModal}
				>
					View Mismatch Report
				</Button>
			</Stack>
			
			{/* Modal Component */}
			<ModalBarChart open={openModal} onClose={handleCloseModal} getData={data} />
		</SectionContainer>
	);
}

export default BarChartSection;
