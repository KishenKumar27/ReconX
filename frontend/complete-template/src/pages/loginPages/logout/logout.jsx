/* eslint-disable import/no-unresolved */
import { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
// MUI
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import logo from '@/assets/images/derivlogo.png';
import Card from '@mui/material/Card';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
// Icons
import LoginIcon from '@mui/icons-material/Login';

function Logout() {
	return (
		<Card
			hover={false}
			elevation={20}
			sx={{
				display: 'block',
				width: {
					xs: '95%',
					sm: '55%',
					md: '35%',
					lg: '25%',
				},
				background: '#fff'
			}}
		>
			<Stack direction="column" spacing={5}>
				<div>
					
					<Typography variant="body2" align='center' color="textSecondary">
					<Box
						component="img"
						src={logo}
						alt="Deriv Logo"
						width={{
							xs: '20vw',
							md: '12vw',
						}}
					/>
					</Typography>
					<Typography variant="h2" align='center'>Thank you</Typography>
				</div>

				<LogoutForm />
			</Stack>
		</Card>
	);
}

function LogoutForm() {
	const navigate = useNavigate();
	const [isLoading, setIsLoading] = useState(false);

	const handleSubmit = async (e) => {
		e.preventDefault();
		console.log('submit');
		setIsLoading(true);
		setTimeout(() => {
			setIsLoading(false);
			navigate('/');
		}, 1000);
	};
	return (
		<form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
			<TextField
				autoFocus
				color="primary"
				name="Email"
				label="Email"
				margin="normal"
				variant="outlined"
				fullWidth
			/>
			<TextField
				color="primary"
				name="password"
				type="password"
				margin="normal"
				label="Password"
				variant="outlined"
				fullWidth
			/>
			<Button
				sx={{
					mt: 2,
					textTransform: 'uppercase',
					color: 'white',
					background: '#000'
				}}
				p={2}
				type="submit"
				variant="contained"
				disabled={isLoading}
				endIcon={
					isLoading ? (
						<CircularProgress
							color="secondary"
							size={25}
							sx={{
								my: 'auto',
							}}
						/>
					) : (
						<LoginIcon />
					)
				}
				fullWidth
				color="secondary"
				hover={false}
			>
				Sign In
			</Button>

			<Typography variant="body2" align='center' color="textSecondary" mt={2}>Forgot password?</Typography>
		</form>
	);
}

export default Logout;
