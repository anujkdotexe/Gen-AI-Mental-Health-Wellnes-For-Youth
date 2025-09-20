import React, { useState, useEffect, useCallback } from 'react';
import { useAppSelector } from '../hooks/redux';
import type { RootState } from '../store/store';

interface CrisisResource {
  id: string;
  name: string;
  phone: string;
  description: string;
  isEmergency: boolean;
  country: string;
}

const CrisisSupport: React.FC = () => {
  const [resources, setResources] = useState<CrisisResource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { token } = useAppSelector((state: RootState) => state.auth);

  const fetchCrisisResources = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/api/crisis/resources', {
        headers: token ? {
          'Authorization': `Bearer ${token}`,
        } : {},
      });

      if (!response.ok) {
        throw new Error('Failed to fetch crisis resources');
      }

      const data = await response.json();
      setResources(data);
    } catch (error: any) {
      setError(error.message || 'Failed to load crisis resources');
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchCrisisResources();
  }, [fetchCrisisResources]);

  const emergencyResources = resources.filter(resource => resource.isEmergency);
  const supportResources = resources.filter(resource => !resource.isEmergency);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-600 mt-2">Loading crisis support resources...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">🆘 Crisis Support</h1>
        <div className="bg-red-50 border border-red-200 text-red-800 px-6 py-4 rounded-lg mb-6">
          <p className="font-semibold text-lg mb-2">🚨 If you're in immediate danger, call emergency services now!</p>
          <p className="text-sm">
            This page provides mental health crisis resources. If you're having thoughts of self-harm 
            or are in immediate danger, please contact emergency services (911, 999, 112) or go to 
            your nearest emergency room.
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Emergency Resources */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-red-700 mb-4">🚨 Emergency Resources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {emergencyResources.map((resource) => (
            <div key={resource.id} className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-red-800 mb-2">{resource.name}</h3>
              <div className="mb-3">
                <a
                  href={`tel:${resource.phone}`}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors inline-block text-lg font-semibold"
                >
                  📞 {resource.phone}
                </a>
              </div>
              <p className="text-red-700 text-sm mb-2">{resource.description}</p>
              <p className="text-red-600 text-xs">📍 {resource.country}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Support Resources */}
      <div>
        <h2 className="text-2xl font-semibold text-blue-700 mb-4">💙 Mental Health Support</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {supportResources.map((resource) => (
            <div key={resource.id} className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">{resource.name}</h3>
              <div className="mb-3">
                <a
                  href={`tel:${resource.phone}`}
                  className="bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-700 transition-colors inline-block"
                >
                  📞 {resource.phone}
                </a>
              </div>
              <p className="text-blue-700 text-sm mb-2">{resource.description}</p>
              <p className="text-blue-600 text-xs">📍 {resource.country}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Additional Support Information */}
      <div className="mt-12 bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-purple-800 mb-4">💜 You're Not Alone</h2>
        <div className="space-y-4 text-purple-700">
          <p>
            <strong>Remember:</strong> Mental health struggles are common and treatable. 
            Seeking help is a sign of strength, not weakness.
          </p>
          
          <div>
            <h3 className="font-semibold mb-2">Warning Signs to Watch For:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Thoughts of suicide or self-harm</li>
              <li>Feeling hopeless or trapped</li>
              <li>Severe depression or anxiety</li>
              <li>Substance abuse</li>
              <li>Social isolation</li>
              <li>Dramatic mood changes</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-2">Immediate Coping Strategies:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Reach out to a trusted friend or family member</li>
              <li>Practice deep breathing or meditation</li>
              <li>Go for a walk in nature</li>
              <li>Listen to calming music</li>
              <li>Write in a journal</li>
              <li>Take a warm bath or shower</li>
            </ul>
          </div>
          
          <div className="mt-6 p-4 bg-purple-100 rounded-lg">
            <h3 className="font-semibold mb-2">🤖 Need to Talk?</h3>
            <p className="text-sm">
              Our AI mental health assistant is available 24/7 for supportive conversations. 
              While not a replacement for professional help, it can provide immediate support 
              and coping strategies.
            </p>
            <a
              href="/ai-chat"
              className="mt-3 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors inline-block"
            >
              Talk to AI Assistant
            </a>
          </div>
        </div>
      </div>

      {/* Privacy Notice */}
      <div className="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 className="font-semibold text-gray-800 mb-2">🔒 Privacy & Confidentiality</h3>
        <p className="text-gray-600 text-sm">
          Your privacy is our priority. All conversations and data are encrypted and secure. 
          However, in cases of immediate risk to yourself or others, emergency services may need 
          to be contacted. Professional counselors and crisis lines maintain strict confidentiality 
          within legal and ethical guidelines.
        </p>
      </div>
    </div>
  );
};

export default CrisisSupport;