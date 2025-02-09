import Card from '@mui/material/Card';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

function TransactionsSection({ data }) {
	return (
		<Card type="none">
			<Stack direction="column" alignItems="flex-between">
				<Typography variant="h5" textTransform="uppercase" m={3}>
					User Transaction History
					{/* <Button
						size="small"
						startIcon={<KeyboardArrowDownIcon />}
						sx={{ m: 1 }}
					>
						Filter by
					</Button> */}
				</Typography>
				<TransactionsTable transactionsData={data} />
			</Stack>
		</Card>
	);
}

const STATUS_CONFIG = {
	success: {
		color: 'success.main',
	},
	error: {
		color: 'error.main',
	},
	warning: {
		color: 'warning.light',
	},
};

function TransactionsTable({ transactionsData }) {

	console.log('transactionsData:', transactionsData[0]);
	return (
		<TableContainer>
			<Table aria-label="transactions table" size="medium">
				<TableHead>
					<TableRow>
						<TableCell align="left">Reconciliation ID</TableCell>
						<TableCell align="left">Transaction ID</TableCell>
						<TableCell align="left">Discrepancy Category</TableCell>
						<TableCell align="left" width={200}>Root Cause</TableCell>
						<TableCell align="left">Resolution Status</TableCell>
						<TableCell align="left">Transaction Date</TableCell>
						<TableCell align="left">Payment Reference</TableCell>
						<TableCell align="left">Amount ($)</TableCell>
						<TableCell align="left">Status</TableCell>
						<TableCell align="left">Gateway Status</TableCell>
						<TableCell align="left">Discrepancy Amount ($)</TableCell>
						<TableCell align="left">Assigned To</TableCell>
						<TableCell align="left">Balance ($)</TableCell>
						<TableCell align="left">Reconciled Balance ($)</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{transactionsData?.map((transaction) => (
						<TransactionRow key={transaction.transaction_id} transaction={transaction} />
					))}
				</TableBody>
			</Table>
		</TableContainer>
	);
}

function TransactionRow({ transaction }) {
	return (
		<TableRow hover>
			<TableCell>{transaction.reconciliation_id}</TableCell>
			<TableCell>{transaction.transaction_id}</TableCell>
			<TableCell>{transaction.discrepancy_category}</TableCell>
			<TableCell>
				<Typography variant="body2" sx={{ whiteSpace: 'pre-line', width: '400px' }}>
					{transaction.root_cause}
				</Typography>
			</TableCell>
			<TableCell>
				<Box
					component="span"
					width={8}
					height={8}
					bgcolor={STATUS_CONFIG[transaction.resolution_status?.toLowerCase()]?.color || '#d3d3d3'}
					borderRadius="50%"
					display="inline-block"
					mr={1}
				/>
				{transaction.resolution_status}
			</TableCell>
			<TableCell>{new Date(transaction.transaction_date).toLocaleDateString()}</TableCell>
			<TableCell>{transaction.payment_reference}</TableCell>
			<TableCell>${transaction.amount}</TableCell>
			<TableCell>{transaction.status ?? 'N/A'}</TableCell>
			<TableCell>{transaction.gateway_status ?? 'N/A'}</TableCell>
			<TableCell>${transaction.discrepancy_amount.toFixed(2)}</TableCell>
			<TableCell>{transaction.assigned_to ?? 'Unassigned'}</TableCell>
			<TableCell>${transaction.balance.toFixed(2)}</TableCell>
			<TableCell>${transaction.reconciled_balance}</TableCell>
		</TableRow>
	);
}

export default TransactionsSection;