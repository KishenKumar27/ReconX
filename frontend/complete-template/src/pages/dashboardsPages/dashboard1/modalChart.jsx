import React, { useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import { Modal, Box, Button, Typography } from '@mui/material';


function ModalBarChart({ getData, open, onClose }) {
    if (!onClose) {
		console.error("⚠️ onClose prop is missing in ModalBarChart");
	}
   const getChartdata = getData.series[0].data;
   const getCategories = getData.xaxis.categories;
  const [chartData] = useState({
    series: [
      {
        data: getChartdata,
      },
    ],
    options: {
      chart: {
        type: 'bar',
        height: 380,
      },
      plotOptions: {
        bar: {
          barHeight: '100%',
          distributed: true,
          horizontal: true,
          dataLabels: {
            position: 'bottom',
          },
        },
      },
      colors: [
        '#33b2df', '#546E7A', '#d4526e', '#13d8aa', '#A5978B',
      ],
      dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
          colors: ['#fff'],
        },
        formatter: (val, opt) => `${opt.w.globals.labels[opt.dataPointIndex]}:  ${val}`,
        offsetX: 10,
        dropShadow: {
          enabled: true,
        },
      },
      stroke: {
        width: 1,
        colors: ['#fff'],
      },
      xaxis: {
        categories: [
          'Missing Payments', 'Amount Mismatch', 'Status Mismatch', 'Duplicates', 'No Discrepancy',
        ],
      },
      yaxis: {
        labels: {
          show: false,
        },
      },
      title: {
        text: 'Dispute Resolution Statistics',
        align: 'center',
        floating: true,
      },
      subtitle: {
        text: 'Category Names as DataLabels inside bars',
        align: 'center',
      },
      tooltip: {
        theme: 'dark',
        x: {
          show: false,
        },
        y: {
          title: {
            formatter: () => '',
          },
        },
      },
    },
  });

  return (
    <Modal open={open} onClose={onClose} >
      <Box sx={{ width: 600, bgcolor: 'white', p: 3, mx: 'auto', mt: 10, borderRadius: 2 }}>
        {/* <Typography variant="h6" mb={2}>Mismatch Report</Typography> */}
        <ReactApexChart options={chartData.options} series={chartData.series} type="bar" height={380} />
        <Button onClick={onClose} sx={{ mt: 2, display: 'block', mx: 'auto' }} variant="contained">Close</Button>
      </Box>
    </Modal>
  );
}

export default ModalBarChart;
