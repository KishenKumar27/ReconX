// MUI
import Typography from '@mui/material/Typography';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';

import PageHeader from '@/components/pageHeader';

function WelcomeSection() {
	return (
		<>
			<PageHeader title="ReconnecX">
				<Breadcrumbs
					aria-label="breadcrumb"
					sx={{
						textTransform: 'uppercase',
					}}
				 />
			</PageHeader>
			<Typography color="text.tertiary"> </Typography>
		</>
	);
}

export default WelcomeSection;
