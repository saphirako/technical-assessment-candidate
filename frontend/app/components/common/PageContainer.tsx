import { Box, Container, ContainerProps } from '@mui/material';
import { ReactNode } from 'react';

interface PageContainerProps
    extends Omit<ContainerProps, 'maxWidth' | 'disableGutters'> {
    children: ReactNode;
    maxWidth?: ContainerProps['maxWidth'];
}

export function PageContainer({
    children,
    maxWidth = 'lg',
    ...containerProps
}: PageContainerProps) {
    return (
        <Container maxWidth={maxWidth} disableGutters {...containerProps}>
            <Box
                marginTop={0}
                marginBottom={6}
                sx={{
                    paddingX: {
                        xs: 1,
                        sm: 2,
                        md: 3,
                        lg: 4,
                        xl: 5,
                    },
                    '& > *:first-of-type': {
                        marginTop: '0 !important',
                    },
                }}
            >
                {children}
            </Box>
        </Container>
    );
}

