import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';

// assets
import logo from '@/assets/images/derivlogo.png';

import LoggedUser from './loggedUser';
import PageHeader from '@/components/pageHeader';

import Breadcrumbs from '@mui/material/Breadcrumbs';
import SearchBar from './searchBar';

function MainHeader() {
	return (
		<Box bgcolor="background.paper" component="header" py={1.5} zIndex={1}>
			<Stack
				component={Container}
				maxWidth="lg"
				direction="row"
				height={50}
				justifyContent="space-between"
				alignItems="center"
				flexWrap="wrap"
				spacing={3}
				overflow="hidden"
			>
				<Stack direction="row" alignItems="center" spacing={1}>
					<Box
						component="img"
						width={{
							xs: 100,
							sm: 150,
						}}
						src={logo}
						alt="logo"
					/>
				</Stack>
				{/* <SearchBar /> */}
				<PageHeader title="ReconX">
				<Breadcrumbs
					aria-label="breadcrumb"
					sx={{
						textTransform: 'uppercase',
					}}
				 />
			</PageHeader>
				<LoggedUser />
			</Stack>
		</Box>
	);
}

export default MainHeader;
