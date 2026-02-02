import { alpha, createTheme, responsiveFontSizes } from '@mui/material';

export const colors = {
    primary: {
        juniper: '#245F31',
        moss: '#D6F1DB',
        tin: '#FFF',
    },
    secondary: {
        fir: '#619C82',
        moss: '#D6F1DB',
        magnesium: '#E8E8E8',
        magnesiumLight: '#F7F7F5',
        cobalt: '#3F69CC',
        cadmium: '#FE4B25',
    },
};

const sharedPalette = {
    primary: {
        main: colors.primary.juniper,
        contrastText: colors.primary.tin,
    },
    secondary: {
        main: colors.secondary.fir,
        contrastText: colors.primary.tin,
    },
    error: {
        main: colors.secondary.cadmium,
        contrastText: colors.primary.tin,
    },
    success: {
        main: alpha(colors.primary.juniper, 0.16),
        contrastText: colors.primary.tin,
    },
    info: {
        main: colors.secondary.cobalt,
        contrastText: colors.primary.tin,
    },
};

const theme = responsiveFontSizes(
    createTheme({
        defaultColorScheme: 'light',
        colorSchemes: {
            light: {
                palette: {
                    ...sharedPalette,
                    common: {
                        black: '#000',
                        white: colors.primary.tin,
                    },
                    text: {
                        primary: colors.primary.juniper,
                        secondary: colors.primary.juniper,
                        disabled: '#B5B5B5',
                    },
                    divider: colors.secondary.magnesium,
                    background: {
                        default: colors.primary.tin,
                        paper: colors.secondary.magnesiumLight,
                    },
                    action: {
                        active: colors.secondary.fir,
                        hover: colors.secondary.magnesium,
                        hoverOpacity: 0.16,
                        selected: colors.secondary.moss,
                        selectedOpacity: 0.08,
                        disabled: '#B5B5B5',
                        disabledBackground: colors.secondary.magnesium,
                        disabledOpacity: 0.38,
                        focus: colors.secondary.moss,
                        focusOpacity: 0.12,
                        activatedOpacity: 0.12,
                    },
                },
            },
        },
        breakpoints: {
            values: {
                xs: 0,
                sm: 600,
                md: 900,
                lg: 1200,
                xl: 1536,
            },
        },
        shape: {
            borderRadius: 8,
        },
        typography: {
            fontFamily: 'system-ui, -apple-system, sans-serif',
            button: {
                textTransform: 'none',
            },
            h1: {
                fontSize: '1.6rem',
            },
            h2: {
                fontSize: '1.15rem',
            },
            h3: {
                fontSize: '1.1rem',
            },
            h4: {
                fontSize: '1.05rem',
            },
            h5: {
                fontSize: '1.025rem',
            },
            h6: {
                fontSize: '1.0125rem',
            },
        },
        components: {},
    })
);

export default theme;

