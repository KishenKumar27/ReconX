/* eslint-disable import/no-unresolved */
/* eslint-disable import/extensions */
// /* eslint-disable import/extensions */
// /* eslint-disable import/no-unresolved */
//  /* eslint-disable import/no-unresolved */
//  /* eslint-disable import/extensions */

// import { useState, useRef, useEffect } from 'react';
// import Typography from '@mui/material/Typography';
// import Box from '@mui/material/Box';
// import Grid from '@mui/material/Grid';
// import Stack from '@mui/material/Stack';
// import Card from '@mui/material/Card';
// import TextField from '@mui/material/TextField';
// import Button from '@mui/material/Button';
// import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
// import AddCard from '@mui/icons-material/AddCard';
// import CardHeader from '@/components/cardHeader';
// import useApiCall from '../../hooks/useApiCall';
// import apiconfig from "../../apiconfig/config.dev";
// import PaymentTableSection from '../../components/paymentTable/index';
// import {
// 	LogoLoader
// } from '@/components/loader';


// // const Pdata = [
// // 	{
// // 	  "Cryptocurrency": [
// // 		{
// // 		  "unique_id": "04404956-a047-4249-8f62-b5937c4c7ad7",
// // 		  "tx_id": "e48e1afe-a9d4-4971-8d7a-05535121d432",
// // 		  "blockchain_platform": "Avalanche",
// // 		  "tx_hash": "1fc7a968-a2c7-47e9-8426-c425ee3b3210",
// // 		  "gateway_verification": "Success",
// // 		  "crypto_value": 1854.08,
// // 		  "gateway_currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-08T06:45:32"
// // 		},
// // 		{
// // 		  "unique_id": "0632ff35-f59a-4f58-b016-b7dbc5afb065",
// // 		  "tx_id": "0b5afda3-072f-47db-bb28-a171390a4b64",
// // 		  "blockchain_platform": "Stellar",
// // 		  "tx_hash": "1dfa2a59-534f-4454-9620-3e1a56093047",
// // 		  "gateway_verification": "Success",
// // 		  "crypto_value": 2336.35,
// // 		  "gateway_currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-07T06:26:32"
// // 		},
// // 		{
// // 		  "unique_id": "0d0902b3-d476-454c-add2-45214b3a3b32",
// // 		  "tx_id": "381c41c0-a33c-436e-b467-85cd5d593bd1",
// // 		  "blockchain_platform": "Polkadot",
// // 		  "tx_hash": "26b7e6cd-2698-454b-bbc2-5bbd26b5d869",
// // 		  "gateway_verification": "Success",
// // 		  "crypto_value": 1673.44,
// // 		  "gateway_currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-05T06:33:32"
// // 		},
// // 		{
// // 		  "unique_id": "10b4802f-342b-4f84-a39f-5d4fd0416553",
// // 		  "tx_id": "a642300f-5af2-4670-8511-4cf0ca393e58",
// // 		  "blockchain_platform": "Hyperledger Fabric",
// // 		  "tx_hash": "7634cad1-eba3-41f9-9b62-e07662df657a",
// // 		  "gateway_verification": "Success",
// // 		  "crypto_value": 1989,
// // 		  "gateway_currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-05T07:00:32"
// // 		},
// // 		{
// // 		  "unique_id": "153e76e9-9413-4b41-8ef4-a8f18c04509d",
// // 		  "tx_id": "307a4997-9498-4f09-9662-a12f75f3b117",
// // 		  "blockchain_platform": "EOSIO",
// // 		  "tx_hash": "4ad95b4e-7dbe-472e-a98f-e83b80dc1f44",
// // 		  "gateway_verification": "Success",
// // 		  "crypto_value": 473.33,
// // 		  "gateway_currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:58:32"
// // 		}
// // 	  ]
// // 	},
// // 	{
// // 	  "E-Wallet": [
// // 		{
// // 		  "unique_id": "0a262fcb-3afc-49ef-a401-5cfb83113143",
// // 		  "tx_id": "ed82f7ca-d8d1-4ea8-804a-40a1646a1d99",
// // 		  "ewallet_platform": "WeChat Pay",
// // 		  "ewallet_tx_id": "035da8fb-c0f6-434b-a107-2da04de5f2ab",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 681.79,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:35:32"
// // 		},
// // 		{
// // 		  "unique_id": "0e57874f-753c-433b-bb86-2496161cf4e2",
// // 		  "tx_id": "328fd3b0-de16-4c68-88de-b424f62e5251",
// // 		  "ewallet_platform": "Touch 'n Go eWallet",
// // 		  "ewallet_tx_id": "77c9c402-fac2-4811-8e3b-cadaec2d0ce9",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 2942.6,
// // 		  "currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-07T06:26:32"
// // 		},
// // 		{
// // 		  "unique_id": "14cd9065-1d74-4271-b64a-bc40761e3e6a",
// // 		  "tx_id": "0bcb706f-1421-4b48-9c3b-fe59e2ce248c",
// // 		  "ewallet_platform": "BigPay",
// // 		  "ewallet_tx_id": "06b9c4d5-f949-43a9-9ea3-8c9aaeb9f828",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 4398.09,
// // 		  "currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:26:32"
// // 		},
// // 		{
// // 		  "unique_id": "1978935a-9295-471f-8480-6d0b6e40098d",
// // 		  "tx_id": "e8e48161-043f-44c4-b5b9-dc9aa5b3362d",
// // 		  "ewallet_platform": "MAE by Maybank",
// // 		  "ewallet_tx_id": "13fdeb7a-fb30-4207-9a47-c14b0167f3d2",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 4662,
// // 		  "currency": "MYR",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:53:32"
// // 		},
// // 		{
// // 		  "unique_id": "1a136a92-4cdd-43ad-a2e2-86b11e9abcd6",
// // 		  "tx_id": "333eb4ea-c1d5-4191-a166-650fc6c429c0",
// // 		  "ewallet_platform": "Alipay",
// // 		  "ewallet_tx_id": "80c87119-af49-45a4-94e2-fe8e64b56f54",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 4473.41,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-07T06:50:32"
// // 		}
// // 	  ]
// // 	},
// // 	{
// // 	  "FPX": [
// // 		{
// // 		  "unique_id": "02ef349a-645d-4c38-a8bd-5a1784abb87c",
// // 		  "tx_id": "833b7a59-fc5a-4629-ad23-c22c51a3a18f",
// // 		  "bank_name": "Alliance Bank",
// // 		  "fpx_tx_id": "3be4317f-1f18-44a2-b078-23e4928fed10",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 3797.35,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-06T06:26:32"
// // 		},
// // 		{
// // 		  "unique_id": "03dfd69e-f39a-4ea7-901f-e5152b2ed1e9",
// // 		  "tx_id": "9245765e-7a35-47bc-85e5-53d6c4538ea3",
// // 		  "bank_name": "Standard Chartered Malaysia",
// // 		  "fpx_tx_id": "2c15a231-433e-4c36-8134-01a49923a88a",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 2807.85,
// // 		  "currency": "MYR",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:55:32"
// // 		},
// // 		{
// // 		  "unique_id": "0528100d-ef2e-434d-a60a-d79c0624ffd6",
// // 		  "tx_id": "0cb9cd12-e9dc-47bf-9ed1-f3314336d068",
// // 		  "bank_name": "HSBC Malaysia",
// // 		  "fpx_tx_id": "76ee9769-a81e-45af-a705-6ce95f535990",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 2366.62,
// // 		  "currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-08T06:33:32"
// // 		},
// // 		{
// // 		  "unique_id": "07932902-40d5-4404-883e-f73033a3012a",
// // 		  "tx_id": "c3be9d3c-da6c-4895-b54e-322fd46894cd",
// // 		  "bank_name": "Agrobank",
// // 		  "fpx_tx_id": "b3f4ac9d-2648-4138-9a1c-3c3e80c0ee23",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 602.31,
// // 		  "currency": "MYR",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:10:32"
// // 		},
// // 		{
// // 		  "unique_id": "08c78cdc-8e18-4349-84bf-36a362be45ad",
// // 		  "tx_id": "60c41166-3d76-444e-b564-701afd07ef59",
// // 		  "bank_name": "UOB Malaysia",
// // 		  "fpx_tx_id": "105d2164-c2ac-468c-9e75-769ea611d342",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 2555.29,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-05T06:30:32"
// // 		}
// // 	  ]
// // 	},
// // 	{
// // 	  "Mobile Payment": [
// // 		{
// // 		  "unique_id": "02c192a8-074c-4f2b-a86e-bb7dcfd35f0a",
// // 		  "tx_id": "62077a46-41dc-4568-9132-483f21907362",
// // 		  "mob_type": "Vodafone",
// // 		  "mob_tx_id": "3ae117f6-dfcc-4853-922e-256b2cda8db5",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 2236.89,
// // 		  "currency": "USD",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-04T06:52:32"
// // 		},
// // 		{
// // 		  "unique_id": "10d2ae00-0956-4f7f-a971-11732223c595",
// // 		  "tx_id": "8fd26dbd-ea12-45b1-b40f-f39a56c3a43f",
// // 		  "mob_type": "Equitel",
// // 		  "mob_tx_id": "3dcb4e69-765d-4756-94bd-eb54cc0b558b",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 1397.59,
// // 		  "currency": "MYR",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-07T06:40:32"
// // 		},
// // 		{
// // 		  "unique_id": "115cee8a-2a88-461f-a038-b3c73937e643",
// // 		  "tx_id": "cd248d89-76c6-43ab-9b2c-04fc00543bfd",
// // 		  "mob_type": "Equitel",
// // 		  "mob_tx_id": "121c1f67-0adb-430c-aa86-54d0138b223f",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 1375.72,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-08T06:08:32"
// // 		},
// // 		{
// // 		  "unique_id": "14e518bf-90d8-416a-a63e-1aa6da1b9561",
// // 		  "tx_id": "acc309b9-7fa6-4e29-8dce-70e4a99bc0a6",
// // 		  "mob_type": "Vodafone",
// // 		  "mob_tx_id": "0284df54-c981-4048-865a-2dc6bc7391b9",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 3231.15,
// // 		  "currency": "MYR",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-07T06:26:32"
// // 		},
// // 		{
// // 		  "unique_id": "199cc78e-f38d-4e52-9a65-bfdd1af648ed",
// // 		  "tx_id": "aaf5f690-62fa-42ec-862f-6a7305e8c0fc",
// // 		  "mob_type": "Airtel",
// // 		  "mob_tx_id": "84a3437d-4742-4bd5-87e7-d67a332ed030",
// // 		  "gateway_verification": "Success",
// // 		  "amount": 4423.57,
// // 		  "currency": "BTC",
// // 		  "gateway_response": "Success",
// // 		  "time_stamp": "2025-02-05T06:44:32"
// // 		}
// // 	  ]
// // 	}
// // ]
  
// function PaymentMethods() {
// 	const getPaymentMethodDataApi = apiconfig.getPaymentMethodUrl || {};
// 	const getPayment4MethodDataApi = apiconfig.getPayment4MethodUrl || {};
// 	const uploadCsvUrl = apiconfig.uploadCsvUrl || {};
// 	const { data: getPaymentMethodData, loadingData: loadingTable } = useApiCall(getPaymentMethodDataApi);
// 	const { data: getPayment4MethodData, loadingData: loading4Table } = useApiCall(getPayment4MethodDataApi);

// 	const isLoading = loadingTable;

	
// 	if (isLoading) {
//         return <Box display="flex" minHeight="100vh" flexDirection="column"><LogoLoader mt={3}/></Box>; // Or use a skeleton UI component
//     }

// 	return (
// 		<Stack spacing={6} mt={3}>
// 			<PaymentMethodsPage getData={getPayment4MethodData} postData={uploadCsvUrl}/>
// 		</Stack>
// 	);
// }

// function PaymentMethodsPage({getData, postData}) {
// 	console.log('getPaymentMethodData:', getData);
// 	const [paymentMethods, setPaymentMethods] = useState([
// 		"crypto_payments",
// 		"e_wallet_transactions",
// 		"fpx_transactions",
// 	]);

// 	const [fileInputVisible, setFileInputVisible] = useState(false);
// 	const [file, setFile] = useState(null);
// 	const fileInputRef = useRef(null);

//     const [uploadSuccess, setUploadSuccess] = useState(false);

// 	const handleAddPaymentMethod = () => {
// 		setPaymentMethods([...paymentMethods, `Payment method ${paymentMethods.length + 1}`]);
// 	};

// 	const handleFileChange = (e) => {
// 		setFile(e.target.files[0]);
// 	};

// 	const handleUploadFile = async () => {
// 		if (!file) {
// 			alert("Please select a file to upload.");
// 			return;
// 		}

// 		// FormData to handle file upload
// 		const formData = new FormData();
// 		formData.append("file", file);

// 		try {
// 			const response = await fetch(postData, {
// 				method: 'POST',
// 				body: formData,
// 			});
// 			if (response.ok) {
// 				alert('File uploaded successfully');

// 				setTimeout(() => {
//                     getPayment4MethodData();
//                 }, 10000);
// 			} else {
// 				alert('Error uploading file');
// 			}
// 		} catch (error) {
// 			alert('Error uploading file');
// 		}

// 		// Reset file input safely
//         setFile(null);
//         if (fileInputRef.current) {
//             fileInputRef.current.value = ""; // Reset file input
//         }
// 	};

// 	useEffect(() => {
//         if (uploadSuccess) {
//             getPayment4MethodData();
//             setUploadSuccess(false); // Reset state
//         }
//     }, [uploadSuccess, getPayment4MethodData]);

// 	const handleGenerate = () => {
		
// 	}

// 	return (
// 		<Card type="section">
// 			<CardHeader title="Payment Methods" />
// 			<Box display="flex" flexDirection="column" alignItems="center">
// 				<form onSubmit={(e) => e.preventDefault()} style={{ display: 'flex', justifyContent: 'center' }}>
// 					<Grid container spacing={2} maxWidth="600px">
// 						{paymentMethods.map((method, index) => (
// 							<Grid item xs={12} key={index}>
// 								<TextField
// 									label={`Payment Method ${index + 1}`}
// 									variant="outlined"
// 									defaultValue={method}
// 									fullWidth
// 								/>
// 							</Grid>
// 						))}
// 					</Grid>
// 				</form>

// 				<Box mt={3} display="flex" justifyContent="center">
// 					<Button
// 						disableElevation
// 						variant="contained"
// 						endIcon={<AutoAwesomeIcon />}
// 						onClick={handleGenerate}
// 						style={{  marginRight: '10px', backgroundColor: '#000', color: '#fff' }}
// 					>
// 						Generate
// 					</Button>

// 					<Button
// 						disableElevation
// 						variant="contained"
// 						endIcon={<AddCard />}
// 						style={{ backgroundColor: '#000', color: '#fff' }}
// 						onClick={() => setFileInputVisible(!fileInputVisible)}
// 					>
// 						Add Payment Method
// 					</Button>
// 				</Box>

// 				{fileInputVisible && (
// 					<Box mt={3} display="flex" justifyContent="center" flexDirection="column" alignItems="center">
// 						<input
// 							type="file"
// 							accept=".csv"
// 							onChange={handleFileChange}
// 						/>
// 						<Button
// 							disableElevation
// 							variant="contained"
// 							onClick={handleUploadFile}
// 							style={{ marginTop: '10px' }}
// 						>
// 							Upload CSV
// 						</Button>
// 					</Box>
// 				)}
// 			</Box>

// 			<Grid container spacing={3} mb={3} mt={2}>
// 					<Grid item xs={12} md={12} lg={12}>
// 						{
// 							Pdata ? (<PaymentTableSection data={Pdata} />) : 'No data found'

// 						}
// 					</Grid>
// 				</Grid>
// 		</Card>
// 	);
// }

// export default PaymentMethods;


// import { useState, useRef, useEffect } from 'react';
// // import Typography from '@mui/material/Typography';
// import Box from '@mui/material/Box';
// import Grid from '@mui/material/Grid';
// import Stack from '@mui/material/Stack';
// import Card from '@mui/material/Card';
// import TextField from '@mui/material/TextField';
// import Button from '@mui/material/Button';
// import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
// import AddCard from '@mui/icons-material/AddCard';
// import CardHeader from '@/components/cardHeader';
// import useApiCall from '../../hooks/useApiCall';
// import apiconfig from "../../apiconfig/config.dev";
// import PaymentTableSection from '../../components/paymentTable/index';
// import {
// 	LogoLoader
// } from '@/components/loader';
  
// function PaymentMethods() {
// 	const getPaymentMethodDataApi = apiconfig.getPaymentMethodUrl || {};
// 	const getPayment4MethodDataApi = apiconfig.getPayment4MethodUrl || {};
// 	const uploadCsvUrl = apiconfig.uploadCsvUrl || {};

// 	// Function to fetch the latest data
// 	const { data: getPaymentMethodData, loadingData: loadingTable } = useApiCall(getPaymentMethodDataApi);
// 	const isLoading = loadingTable;
	
// 	const [payment4MethodData, setPayment4MethodData] = useState([]);

// 	// Function to fetch latest Payment 4 Method Data
// 	const fetchPaymentData = async () => {
// 		try {
// 			const response = await fetch(getPayment4MethodDataApi);
// 			const data = await response.json();
// 			setPayment4MethodData(data);
// 		} catch (error) {
// 			console.error("Error fetching Payment 4 Method Data:", error);
// 		}
// 	};

// 	// Fetch data initially
// 	useEffect(() => {
// 		fetchPaymentData();
// 	}, []);


// 	if (isLoading) {
//         return <Box display="flex" minHeight="100vh" flexDirection="column"><LogoLoader mt={3}/></Box>; 
//     }

// 	return (
// 		<Stack spacing={6} mt={3}>
// 			<PaymentMethodsPage getData={payment4MethodData} postData={uploadCsvUrl} refetchData={fetchPayment4MethodData}/>
// 		</Stack>
// 	);
// }

// function PaymentMethodsPage({getData, postData, refetchData}) {
// 	console.log('getPayment4MethodData:', getData);
// 	const [paymentMethods, setPaymentMethods] = useState([
// 		"crypto_payments",
// 		"e_wallet_transactions",
// 		"fpx_transactions",
// 	]);

// 	const [fileInputVisible, setFileInputVisible] = useState(false);
// 	const [file, setFile] = useState(null);
// 	const fileInputRef = useRef(null);
// 	const [uploadSuccess, setUploadSuccess] = useState(false);

// 	const handleFileChange = (e) => {
// 		setFile(e.target.files[0]);
// 	};

// 	const handleUploadFile = async () => {
// 		if (!file) {
// 			alert("Please select a file to upload.");
// 			return;
// 		}

// 		const formData = new FormData();
// 		formData.append("file", file);

// 		try {
// 			const response = await fetch(postData, {
// 				method: 'POST',
// 				body: formData,
// 			});

// 			if (response.ok) {
// 				alert('File uploaded successfully');
// 				setUploadSuccess(true); // Trigger the refetch

// 				setTimeout(() => {
//                     refetchData(); // Fetch the latest data after 10 seconds
//                 }, 10000);
// 			} else {
// 				alert('Error uploading file');
// 			}
// 		} catch (error) {
// 			alert('Error uploading file');
// 		}

// 		// Reset file input safely
// 		setFile(null);
// 		if (fileInputRef.current) {
// 			fileInputRef.current.value = "";
// 		}
// 	};



// 	const handleGenerate = () => {
// 		// Functionality for generating something
// 	};

// 	return (
// 		<Card type="section">
// 			<CardHeader title="Payment Methods" />
// 			<Box display="flex" flexDirection="column" alignItems="center">
// 				<form onSubmit={(e) => e.preventDefault()} style={{ display: 'flex', justifyContent: 'center' }}>
// 					<Grid container spacing={2} maxWidth="600px">
// 						{paymentMethods.map((method, index) => (
// 							<Grid item xs={12} key={index}>
// 								<TextField
// 									label={`Payment Method ${index + 1}`}
// 									variant="outlined"
// 									defaultValue={method}
// 									fullWidth
// 								/>
// 							</Grid>
// 						))}
// 					</Grid>
// 				</form>

// 				<Box mt={3} display="flex" justifyContent="center">
// 					<Button
// 						disableElevation
// 						variant="contained"
// 						endIcon={<AutoAwesomeIcon />}
// 						onClick={handleGenerate}
// 						style={{ marginRight: '10px', backgroundColor: '#000', color: '#fff' }}
// 					>
// 						Generate
// 					</Button>

// 					<Button
// 						disableElevation
// 						variant="contained"
// 						endIcon={<AddCard />}
// 						style={{ backgroundColor: '#000', color: '#fff' }}
// 						onClick={() => setFileInputVisible(!fileInputVisible)}
// 					>
// 						Add Payment Method
// 					</Button>
// 				</Box>

// 				{fileInputVisible && (
// 					<Box mt={3} display="flex" justifyContent="center" flexDirection="column" alignItems="center">
// 						<input type="file" accept=".csv" onChange={handleFileChange} />
// 						<Button
// 							disableElevation
// 							variant="contained"
// 							onClick={handleUploadFile}
// 							style={{ marginTop: '10px' }}
// 						>
// 							Upload CSV
// 						</Button>
// 					</Box>
// 				)}
// 			</Box>

// 			<Grid container spacing={3} mb={3} mt={2}>
// 				<Grid item xs={12} md={12} lg={12}>
// 					{getData ? <PaymentTableSection data={getData} /> : 'No data found'}
// 				</Grid>
// 			</Grid>
// 		</Card>
// 	);
// }

// export default PaymentMethods;


import { useState, useRef, useEffect } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Card from '@mui/material/Card';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import AddCard from '@mui/icons-material/AddCard';
import CardHeader from '@/components/cardHeader';
import useApiCall from '../../hooks/useApiCall';
import apiconfig from "../../apiconfig/config.dev";
import PaymentTableSection from '../../components/paymentTable/index';
import { LogoLoader } from '@/components/loader';

function PaymentMethods() {
	const getPaymentMethodDataApi = apiconfig.getPaymentMethodUrl || "";
	const getPayment4MethodDataApi = apiconfig.getPayment4MethodUrl || "";
	const getconsolidatedtableApi = apiconfig.consolidatedtable || "";
	const uploadCsvUrl = apiconfig.uploadCsvUrl || "";

	const { data: getPaymentMethodData, loadingData: loadingTable } = useApiCall(getPaymentMethodDataApi);
	const { data: getPayment4MethodData } = useApiCall(getPayment4MethodDataApi);
	const { data: getconsolidatedtable } = useApiCall(getconsolidatedtableApi);
	const [payment4MethodData, setPayment4MethodData] = useState([]);

	// Function to fetch the latest payment method data
	const fetchPaymentData = async () => {
		try {
			const response = await fetch(getPayment4MethodDataApi);
			if (!response.ok) throw new Error("Failed to fetch data");
			const data = await response.json();
			setPayment4MethodData(data);
		} catch (error) {
			console.error("Error fetching Payment 4 Method Data:", error);
		}
	};

	// Fetch data on mount
	useEffect(() => {
		fetchPaymentData();
	}, []);

	if (loadingTable) {
		return <Box display="flex" minHeight="100vh" flexDirection="column"><LogoLoader mt={3} /></Box>;
	}

	return (
		<Stack spacing={6} mt={3}>
			<PaymentMethodsPage 
				getData={payment4MethodData} 
				postData={uploadCsvUrl} 
				refetchData={fetchPaymentData} // Passing function correctly
			/>
		</Stack>
	);
}

function PaymentMethodsPage({ getData, postData, refetchData }) {
	const [paymentMethods, setPaymentMethods] = useState([
		"crypto_payments",
		"e_wallet_transactions",
		"fpx_transactions",
	]);

	const [file, setFile] = useState(null);
	const [fileInputVisible, setFileInputVisible] = useState(false);
	const fileInputRef = useRef(null);
	const [showButton, setShowButton] = useState(false);


	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

	const handleUploadFile = async () => {
		if (!file) {
			alert("Please select a file to upload.");
			return;
		}

		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch(postData, {
				method: 'POST',
				body: formData,
			});

			if (response.ok) {
				alert('File uploaded successfully');
				
				// Fetch new data after 10 seconds
				setTimeout(() => {
					if (typeof refetchData === "function") {
						refetchData(); // Fetch updated data
						setShowButton(true);
					} else {
						console.error("refetchData is not a function");
					}
				}, 10000);
			} else {
				alert('Error uploading file');
			}
		} catch (error) {
			alert('Error uploading file');
		}

		// Reset file input safely
		setFile(null);
		if (fileInputRef.current) {
			fileInputRef.current.value = "";
		}
	};

	const handleAddPaymentMethod = () => {
		setPaymentMethods([...paymentMethods, `Payment method ${paymentMethods.length + 1}`]);
	};

	return (
		<Card type="section">
			<CardHeader title="Payment Methods" />
			<Box display="flex" flexDirection="column" alignItems="center">
				<form onSubmit={(e) => e.preventDefault()} style={{ display: 'flex', justifyContent: 'center' }}>
					<Grid container spacing={2} maxWidth="600px">
						{paymentMethods.map((method, index) => (
							<Grid item xs={12} key={index}>
								<TextField
									label={`Payment Method ${index + 1}`}
									variant="outlined"
									defaultValue={method}
									fullWidth
								/>
							</Grid>
						))}
					</Grid>
				</form>

				<Box mt={3} display="flex" justifyContent="center">
					{showButton &&
						<Button
							disableElevation
							variant="contained"
							endIcon={<AutoAwesomeIcon />}
							style={{ marginRight: '10px', backgroundColor: '#000', color: '#fff' }}
						>
							Generate
						</Button>
					}

					<Button
						disableElevation
						variant="contained"
						endIcon={<AddCard />}
						style={{ backgroundColor: '#000', color: '#fff' }}
						onClick={() => setFileInputVisible(!fileInputVisible)}
					>
						Add Payment Method
					</Button>
				</Box>

				{fileInputVisible && (
					<Box mt={3} display="flex" justifyContent="center" flexDirection="column" alignItems="center">
						<input
							type="file"
							accept=".csv"
							onChange={handleFileChange}
						/>
						<Button
							disableElevation
							variant="contained"
							onClick={handleUploadFile}
							style={{ marginTop: '10px' }}
						>
							Upload CSV
						</Button>
					</Box>
				)}
			</Box>

			<Grid container spacing={3} mb={3} mt={2}>
				<Grid item xs={12} md={12} lg={12}>
					{getData.length > 0 ? <PaymentTableSection data={getData} /> : 'No data found'}
				</Grid>
			</Grid>

			
		</Card>
	);
}

export default PaymentMethods;

