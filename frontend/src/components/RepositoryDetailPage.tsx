import React from 'react';

interface RepositoryDetailPageProps {
  repo: {
    id: string;
    full_name: string;
    content: string;
    interval: number;
    is_active: boolean;
  };
}


export default function RepositoryDetailPage({ repo }: RepositoryDetailPageProps) {
  return (
    <div>
      <main className='bg-white p-6'>
        <div className="container mx-auto px-4 py-8">
          <p>{repo.id}</p>
          <p>{repo.full_name}</p>
        </div>
      </main>
    </div>
  );
} 