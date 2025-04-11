import React, { useState } from 'react';

interface CreateSwitchFormProps {
  userEmail: string;
}

export default function CreateSwitchForm({ userEmail }: CreateSwitchFormProps) {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);
    
    const switchData = {
      user_email: userEmail,
      name: formData.get('name')?.toString() || '',
      content: formData.get('content')?.toString() || '',
      interval: parseInt(formData.get('interval')?.toString() || '0', 10)
    };
    
    try {
      const response = await fetch('http://localhost:8000/switches', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(switchData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to create switch');
      }
      
      alert('Switch created successfully');
      window.location.href = '/switches'; // Redirect to switches list
      
    } catch (error) {
      console.error('Error creating switch:', error);
      alert(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Create New Switch</h1>
      
      <form className="max-w-2xl space-y-6" onSubmit={handleSubmit}>
        <div className="space-y-2">
          <label htmlFor="name" className="block font-bold">Switch Name</label>
          <input 
            type="text" 
            id="name" 
            name="name" 
            className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
            required
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="content" className="block font-bold">Content</label>
          <textarea 
            id="content" 
            name="content" 
            rows={4} 
            className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
            required
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="interval" className="block font-bold">Interval (days)</label>
          <input 
            type="number" 
            id="interval" 
            name="interval" 
            min="1"
            className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
            required
          />
        </div>

        <button 
          type="submit" 
          className="border-2 border-black dark:border-white bg-white dark:bg-black text-black dark:text-white px-4 py-2 font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0)] dark:shadow-[2px_2px_0px_0px_rgba(255,255,255)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[1px_1px_0px_0px_rgba(0,0,0)] dark:hover:shadow-[1px_1px_0px_0px_rgba(255,255,255)] transition-all"
        >
          Create Switch
        </button>
      </form>
    </div>
  );
} 