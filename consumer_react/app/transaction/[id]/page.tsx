import TransactionDetail from "./TransactionDetail";

interface PageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function Page({ params }: PageProps) {
  const resolvedParams = await params;
  return <TransactionDetail id={resolvedParams.id} />;
}
