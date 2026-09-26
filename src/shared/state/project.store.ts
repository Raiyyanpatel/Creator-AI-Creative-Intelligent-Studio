import { useState, useEffect } from 'react';
import { Project } from '@/shared/types/project';
import { storage } from '@/utils/storage';

const INITIAL_PROJECTS: Project[] = [
  {
    id: 'p1',
    title: 'Building with AI Agents',
    description: 'On-device automated coding agents demonstration on mobile silicon.',
    thumbnailUrl: '/assets/create-edit-video.jpg',
    durationSeconds: 42,
    aspectRatio: '9:16',
    updatedAt: 'Edited today',
    status: 'draft',
    clips: [
      {
        id: 'c1',
        mediaUrl: '/assets/create-edit-video.jpg',
        title: 'Main Speaker Intro',
        start: 0,
        duration: 22,
        cutIn: 0,
        cutOut: 22,
        speed: 1,
        volume: 1,
      },
      {
        id: 'c2',
        mediaUrl: '/assets/trend-on-device-ai.jpg',
        title: 'B-Roll Benchmark Demo',
        start: 22,
        duration: 20,
        cutIn: 0,
        cutOut: 20,
        speed: 1,
        volume: 0.8,
      },
    ],
  },
  {
    id: 'p2',
    title: 'On-device AI explained',
    description: 'Why localized models outperform remote servers for creators.',
    thumbnailUrl: '/assets/trend-on-device-ai.jpg',
    durationSeconds: 78,
    aspectRatio: '9:16',
    updatedAt: 'Yesterday',
    status: 'ready',
    clips: [],
  },
  {
    id: 'p3',
    title: 'Mumbai Tech Walk',
    description: 'Vlog testing camera stabilization and mobile teleprompter.',
    thumbnailUrl: '/assets/create-from-idea.jpg',
    durationSeconds: 31,
    aspectRatio: '9:16',
    updatedAt: '3 days ago',
    status: 'ready',
    clips: [],
  },
];

let projects: Project[] = storage.load('projects_list', INITIAL_PROJECTS);
let activeProjectId: string = projects[0]?.id || 'p1';
const listeners = new Set<() => void>();

function notify() {
  storage.save('projects_list', projects);
  listeners.forEach((l) => l());
}

export const projectStore = {
  getProjects: () => projects,
  getActiveProject: () => projects.find((p) => p.id === activeProjectId) || projects[0],
  setActiveProjectId: (id: string) => {
    activeProjectId = id;
    notify();
  },
  addProject: (newProj: Partial<Project>) => {
    const p: Project = {
      id: `proj_${Date.now()}`,
      title: newProj.title || 'Untitled Project',
      description: newProj.description || '',
      thumbnailUrl: newProj.thumbnailUrl || '/assets/create-edit-video.jpg',
      durationSeconds: newProj.durationSeconds || 30,
      aspectRatio: newProj.aspectRatio || '9:16',
      updatedAt: 'Just now',
      status: 'draft',
      clips: newProj.clips || [],
      knowledge: newProj.knowledge,
    };
    projects = [p, ...projects];
    activeProjectId = p.id;
    notify();
    return p;
  },
  updateActiveProject: (partial: Partial<Project>) => {
    projects = projects.map((p) => (p.id === activeProjectId ? { ...p, ...partial } : p));
    notify();
  },
};

export function useProjectStore() {
  const [, setVersion] = useState(0);
  useEffect(() => {
    const update = () => setVersion((v) => v + 1);
    listeners.add(update);
    return () => {
      listeners.delete(update);
    };
  }, []);

  return {
    projects,
    activeProject: projectStore.getActiveProject(),
    setActiveProjectId: projectStore.setActiveProjectId,
    addProject: projectStore.addProject,
    updateActiveProject: projectStore.updateActiveProject,
  };
}
