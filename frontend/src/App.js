import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProjectRequirementsForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    business_context: "",
    success_criteria: "",
    constraints: "",
    stakeholders: "",
    timeline_preference: "",
    budget_range: ""
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Project Requirements Input</h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project Title *
          </label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter project title"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project Description *
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Describe the project in detail..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Business Context *
          </label>
          <textarea
            name="business_context"
            value={formData.business_context}
            onChange={handleChange}
            required
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Why is this project important? What business problem does it solve?"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Success Criteria *
          </label>
          <textarea
            name="success_criteria"
            value={formData.success_criteria}
            onChange={handleChange}
            required
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="How will you measure project success?"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Constraints *
          </label>
          <textarea
            name="constraints"
            value={formData.constraints}
            onChange={handleChange}
            required
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Any limitations, restrictions, or constraints?"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Key Stakeholders *
          </label>
          <input
            type="text"
            name="stakeholders"
            value={formData.stakeholders}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Who are the key stakeholders? (comma separated)"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Timeline Preference *
          </label>
          <input
            type="text"
            name="timeline_preference"
            value={formData.timeline_preference}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., 3 months, ASAP, flexible, by Q2 2025"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Budget Range (Optional)
          </label>
          <input
            type="text"
            name="budget_range"
            value={formData.budget_range}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., $50K - $100K, unlimited, to be determined"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              AI is Analyzing & Planning...
            </div>
          ) : (
            "Generate AI Project Plan"
          )}
        </button>
      </form>
    </div>
  );
};

const ProjectPlanDisplay = ({ plan }) => {
  if (!plan) return null;

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">AI-Generated Project Plan</h2>
        <div className="flex items-center space-x-4">
          <span className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm">
            Timeline: {plan.timeline_weeks} weeks
          </span>
          <span className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm">
            Confidence: {Math.round(plan.confidence_score * 100)}%
          </span>
        </div>
      </div>

      {/* SMART Objectives */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">SMART Objectives</h3>
        <div className="space-y-4">
          {plan.objectives.map((obj, index) => (
            <div key={index} className="border-l-4 border-blue-500 pl-4">
              <h4 className="font-semibold text-gray-800">{obj.objective}</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-3 text-sm">
                <div><strong>Specific:</strong> {obj.specific}</div>
                <div><strong>Measurable:</strong> {obj.measurable}</div>
                <div><strong>Achievable:</strong> {obj.achievable}</div>
                <div><strong>Relevant:</strong> {obj.relevant}</div>
                <div><strong>Time-bound:</strong> {obj.time_bound}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Work Breakdown Structure */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Work Breakdown Structure (WBS)</h3>
        <div className="space-y-3">
          {plan.wbs_tasks.map((task) => (
            <div key={task.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold text-gray-800">{task.name}</h4>
                <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-3">{task.description}</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div><strong>Estimated Hours:</strong> {task.estimated_hours}</div>
                <div><strong>Assigned Role:</strong> {task.assigned_role}</div>
                <div><strong>Level:</strong> {task.level}</div>
              </div>
              {task.dependencies.length > 0 && (
                <div className="mt-2 text-sm">
                  <strong>Dependencies:</strong> {task.dependencies.join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Resource Estimates */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Resource Estimates</h3>
        <div className="overflow-x-auto">
          <table className="w-full table-auto">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left">Role</th>
                <th className="px-4 py-2 text-left">Hours Required</th>
                <th className="px-4 py-2 text-left">Skill Level</th>
                <th className="px-4 py-2 text-left">Cost Estimate</th>
              </tr>
            </thead>
            <tbody>
              {plan.resource_estimates.map((resource, index) => (
                <tr key={index} className="border-t">
                  <td className="px-4 py-2 font-medium">{resource.role}</td>
                  <td className="px-4 py-2">{resource.hours_required}</td>
                  <td className="px-4 py-2">{resource.skill_level}</td>
                  <td className="px-4 py-2">
                    {resource.cost_estimate ? `$${resource.cost_estimate.toLocaleString()}` : 'TBD'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Risk Analysis */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Risk Analysis</h3>
        <div className="space-y-4">
          {plan.risk_analysis.map((risk, index) => (
            <div key={index} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-semibold text-gray-800">{risk.risk}</h4>
                <div className="flex space-x-2 text-sm">
                  <span className={`font-medium ${getRiskColor(risk.probability)}`}>
                    P: {risk.probability}
                  </span>
                  <span className={`font-medium ${getRiskColor(risk.impact)}`}>
                    I: {risk.impact}
                  </span>
                </div>
              </div>
              <p className="text-gray-600 text-sm mb-2">{risk.mitigation_strategy}</p>
              <div className="text-sm"><strong>Owner:</strong> {risk.owner}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Success Metrics & Next Steps */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4 text-gray-800">Success Metrics</h3>
          <ul className="space-y-2">
            {plan.success_metrics.map((metric, index) => (
              <li key={index} className="flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                {metric}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4 text-gray-800">Next Steps</h3>
          <ol className="space-y-2">
            {plan.next_steps.map((step, index) => (
              <li key={index} className="flex items-start">
                <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 mt-1">
                  {index + 1}
                </span>
                {step}
              </li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      // Submit project requirements
      const requirementsResponse = await axios.post(`${API}/project-requirements`, formData);
      const requirementsId = requirementsResponse.data.id;
      
      // Generate AI project plan
      const planResponse = await axios.post(`${API}/generate-plan/${requirementsId}`);
      setCurrentPlan(planResponse.data);
      
    } catch (err) {
      console.error('Error generating project plan:', err);
      setError(err.response?.data?.detail || 'Failed to generate project plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🤖 Autonomous AI Project Manager
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Advanced AI system that completely replaces human project managers. 
            Submit your project requirements and watch AI generate comprehensive plans faster and more accurately than any human PM.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Main Content */}
        {!currentPlan ? (
          <ProjectRequirementsForm onSubmit={handleFormSubmit} loading={loading} />
        ) : (
          <div>
            <div className="mb-6 text-center">
              <button
                onClick={() => setCurrentPlan(null)}
                className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                ← Create New Project Plan
              </button>
            </div>
            <ProjectPlanDisplay plan={currentPlan} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
