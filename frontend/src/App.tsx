import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { AgentWorkspacePage } from "./pages/AgentWorkspacePage"
import { OverviewPage } from "./pages/OverviewPage"
import { RepositoriesPage } from "./pages/RepositoriesPage"
import { SecurityPage } from "./pages/SecurityPage"
import { CodeQualityPage } from "./pages/CodeQualityPage"
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/repositories" element={<RepositoriesPage />} />
       <Route path="/security" element={<SecurityPage />} />
       <Route path="/quality" element={<CodeQualityPage />} />
        <Route
          path="/quality"
          element={
            <AgentWorkspacePage
              title="Code Quality"
              subtitle="Maintainability and complexity analysis will live here."
              agentId="code-quality"
              capability="This workspace will later display real quality metrics from the Code Quality Agent."
            />
          }
        />
        <Route
          path="/refactoring"
          element={
            <AgentWorkspacePage
              title="Refactoring"
              subtitle="Guarded structural change plans will live here."
              agentId="refactoring"
              capability="This workspace will later display proposed diffs after the Refactoring Agent is implemented."
            />
          }
        />
        <Route
          path="/prediction"
          element={
            <AgentWorkspacePage
              title="Predictive Maintenance"
              subtitle="Risk forecasts will live here after models are trained."
              agentId="predictive-maintenance"
              capability="This workspace will later display forecasts from the Predictive Maintenance Agent."
            />
          }
        />
        <Route
          path="/operations"
          element={
            <AgentWorkspacePage
              title="Autonomous Operations"
              subtitle="Orchestration, validation, and rollback will live here."
              agentId="orchestrator"
              capability="This workspace will later coordinate the Autonomous Orchestrator, Validation Agent, and rollback system."
            />
          }
        />
        <Route
          path="/reports"
          element={
            <AgentWorkspacePage
              title="Reports"
              subtitle="Audit-ready engineering reports will live here."
              agentId="reporting"
              capability="This workspace will later render generated reports. None exist yet because no analysis has run."
            />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
