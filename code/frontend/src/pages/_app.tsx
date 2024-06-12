import { type AppType } from "next/dist/shared/lib/utils";
import { ThemeProvider } from "~/components/ThemeProvider";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "~/styles/globals.css";

const MyApp: AppType = ({ Component, pageProps }) => {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <Component {...pageProps} />
      <ToastContainer />
    </ThemeProvider>
  );
};

export default MyApp;
