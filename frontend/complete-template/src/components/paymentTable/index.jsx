/* eslint-disable no-unused-vars */

import React from 'react';
import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';

function formatCell(value, col) {
  if (col.includes('time_stamp')) {
    return new Date(value).toLocaleString();
  }
  if (typeof value === 'number') {
    return value.toFixed(2);
  }
  return value || 'N/A';
}

function formatTitle(key) {
  return key.replace(/_/g, ' ').replace(/logs?/i, '').trim().toUpperCase();
}

function PaymentTable({ data }) {
  console.log('Payment Table Data:', data);

  if (!data || !Array.isArray(data) || data.length === 0) {
    return <Typography variant="h6" color="error" align='center' mt={3}>No transaction data available.</Typography>;
  }

  return (
    <Card sx={{ p: 2 }}>
      <Typography variant="h5" textTransform="uppercase" gutterBottom>
        Payment Methods
      </Typography>
      {data.map((dataItem, index) => (
        <div key={index}>
          {Object.keys(dataItem).map((category) => (
            <PaymentTableSection key={`${index}-${category}`} title={formatTitle(category)} transactionsData={dataItem[category]} />
          ))}
        </div>
      ))}
    </Card>
  );
}

function PaymentTableSection({ title, transactionsData }) {
  console.log(`Data for ${title}:`, transactionsData);
  
  if (!Array.isArray(transactionsData) || transactionsData.length === 0) {
    return null;
  }

  return (
    <Stack spacing={2} mt={3}>
      <Typography variant="h6">{title}</Typography>
      <TableContainer>
        <Table>
          {transactionsData.length > 0 && (
            <TableHead>
              <TableRow>
                {Object.keys(transactionsData[0]).map((key) => (
                  <TableCell key={key}>{formatTitle(key)}</TableCell>
                ))}
              </TableRow>
            </TableHead>
          )}
          <TableBody>
            {transactionsData.map((row, index) => (
              <TableRow key={index}>
                {Object.keys(row).map((col) => (
                  <TableCell key={col}>{formatCell(row[col], col)}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}

export default PaymentTable;
