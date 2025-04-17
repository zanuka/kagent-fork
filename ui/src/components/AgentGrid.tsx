import type { AgentResponse } from '@/types/datamodel';
import { AgentCard } from './AgentCard';

interface AgentGridProps {
  agentResponse: AgentResponse[];
}

export function AgentGrid({ agentResponse }: AgentGridProps) {
  if (!agentResponse || !Array.isArray(agentResponse)) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {agentResponse
        .filter((item) => item?.agent?.metadata)
        .map((item) => (
          <AgentCard
            key={item.agent.metadata.name}
            agentResponse={item}
            id={item.id}
          />
        ))}
    </div>
  );
}
