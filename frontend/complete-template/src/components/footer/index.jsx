import constants from '@/utils/constants';
// MUI
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Link from '@mui/material/Link';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import Button from '@mui/material/Button';

// Icons
import FacebookIcon from '@mui/icons-material/Facebook';
import GitHubIcon from '@mui/icons-material/GitHub';
import TwitterIcon from '@mui/icons-material/Twitter';
import GoogleIcon from '@mui/icons-material/Google';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import LocalPhoneOutlinedIcon from '@mui/icons-material/LocalPhoneOutlined';
import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined';
// assets
import logo from '@/assets/images/logo/png/Color_logo_nobg.png';

function Footer() {
	return (
		<Box bgcolor={(theme) => theme.palette.background.paper} py={3} borderTop={1} borderColor="black.300">
			<Container maxWidth="lg" component={Stack} direction="column" spacing={5}>

				{/* <Divider
					variant="middle"
					sx={{
						bgcolor: (theme) => theme.palette.secondary.main,
					}}
				/> */}
				<Stack direction={{ lg: 'row' }} justifyContent="space-between" alignItems="center" flexWrap="wrap">
					<Typography variant="body1" textAlign="center">
						Copyright 2025 © All Rights Reserved.
					</Typography>
					<Typography variant="subtitle1" textAlign="center">
						Code Lah - AI Hackathon by 
						<Link
							underline="hover"
							sx={{
								cursor: 'pointer',
							}}
							href="https://deriv.com/hackathon"
							target="_blank"
							rel="noreferrer noopener"
							fontWeight="medium"
							color="red"
						>
							 {' '}Deriv
						</Link>
					</Typography>
				</Stack>
			</Container>
		</Box>
	);
}

function ContactLink({ Icon, text }) {
	return (
		<Stack spacing={1} alignItems="center" direction="row">
			<Icon
				color="primary"
				sx={{
					mr: 3,
				}}
			/>
			<Typography variant="body1">{text}</Typography>
		</Stack>
	);
}

function FooterLink({ text }) {
	return (
		<Link
			variant="body2"
			fontWeight="300"
			href="#!"
			underline="hover"
			sx={{
				color: 'text.primary',
				'&:hover': {
					'& svg': {
						opacity: '1',
						ml: 2,
					},
				},
				'&::before': {
					content: '""',
					display: 'inline-block',
					borderRadius: '50%',
					bgcolor: 'primary.main',
					width: '4px',
					height: '4px',
					mb: '2px',
					mr: 2,
				},
			}}
		>
			{/* <span style={{ marginRight: '15px' }}>•</span> */}
			{text}
			<ArrowForwardIosIcon
				color="primary"
				sx={{
					transition: '0.3s',
					fontSize: '11px',
					ml: 0,
					opacity: '0',
				}}
			/>
		</Link>
	);
}

export default Footer;
