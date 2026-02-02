import { Box, Stack, Typography } from '@mui/material';
import { PageContainer } from 'app/components/common/PageContainer';

export default function Home() {
    return (
        <PageContainer>
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minHeight: '60vh',
                    textAlign: 'center',
                    py: 6,
                }}
            >
                <Stack spacing={3} sx={{ maxWidth: 600 }}>
                    <Typography variant="h1" component="h1">
                        Product Replacement Search
                    </Typography>
                    <Box
                        sx={{
                            mt: 4,
                            p: 3,
                            bgcolor: 'background.paper',
                            borderRadius: 2,
                            border: '1px dashed',
                            borderColor: 'divider',
                        }}
                    >
                        <Typography variant="body2" color="text.secondary" fontStyle="italic">
                            TODO: Implement your search interface and results display. Feel free to modify this page and any other frontend files as needed.
                        </Typography>
                    </Box>
                </Stack>
            </Box>
        </PageContainer>
    );
}
