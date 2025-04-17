import { AgentsProvider } from '@/components/AgentsProvider';
import { Footer } from '@/components/Footer';
import { Header } from '@/components/Header';
import { ThemeProvider } from '@/components/ThemeProvider';
import { Toaster } from '@/components/ui/sonner';
import { TooltipProvider } from '@/components/ui/tooltip';
import type { Metadata } from 'next';
import { Geist } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'kagent.dev | Solo.io',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.className} flex flex-col h-screen overflow-hidden`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <TooltipProvider>
            <AgentsProvider>
              <Header />
              <main className="flex-1 overflow-y-scroll w-full mx-auto">
                {children}
              </main>
              <Footer />
              <Toaster />
            </AgentsProvider>
          </TooltipProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
