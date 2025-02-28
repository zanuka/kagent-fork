"use client";

import AgentList from "@/components/AgentList";
import { AgentsProvider, useAgents } from "@/components/AgentsProvider";
import { ErrorState } from "@/components/ErrorState";
import { LoadingState } from "@/components/LoadingState";

function AgentListContent() {
  const { teams, loading, error } = useAgents();

  return (
    <>
      {error ? (
        <ErrorState message={error} />
      ) : (
        <AgentList teams={teams || []} />
      )}
      {loading && <LoadingState />}
    </>
  );
}
export default function AgentListPage() {
  return (
    <AgentsProvider>
      <AgentListContent />
    </AgentsProvider>
  );
}
