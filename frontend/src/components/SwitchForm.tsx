import React from 'react';

interface SwitchFormProps {
  switchItem: {
    id: string;
    name: string;
    content: string;
    interval: number;
    is_active: boolean;
  };
}

export default function SwitchForm({ switchItem }: SwitchFormProps) {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const form = e.currentTarget;
    const formData = new FormData(form);
    
    const switchData = {
      name: formData.get('name')?.toString() || '',
      content: formData.get('content')?.toString() || '',
      interval: parseInt(formData.get('interval')?.toString() || '0', 10),
      is_active: formData.get('active') === 'true',
    };
    
    try {
      console.log('Sending data:', switchData);
      const response = await fetch(`http://localhost:8000/switches/update/${switchItem.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(switchData)
      });
      
      // Log the response for debugging
      console.log('Response status:', response.status);
      const responseData = await response.json();
      console.log('Response data:', responseData);
      
      if (!response.ok) {
        throw new Error(responseData.message || 'Failed to update switch');
      }
      
      alert('Switch updated successfully');
      window.location.href = '/switches'; // Redirect after successful update
      
    } catch (error) {
      console.error('Error updating switch:', error);
      alert(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  };

  const handleCancel = () => {
    window.location.href = '/switches';
  };

  return (
    <main className='bg-white p-6'>
      <div className="container mx-auto px-4 py-8">
        <form id="switchForm" className="max-w-2xl space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label htmlFor="name" className="block font-bold">Switch Name</label>
            <input 
              type="text" 
              id="name"
              name="name" 
              defaultValue={switchItem.name} 
              className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="content" className="block font-bold">Content</label>
            <textarea 
              id="content"
              name="content" 
              defaultValue={switchItem.content} 
              className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
              rows={4}
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
              defaultValue={switchItem.interval}
              className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="active" className="block font-bold">Status</label>
            <select
              id="active"
              name="active"
              defaultValue={switchItem.is_active.toString()}
              className="w-full p-2 border-2 border-black dark:border-white bg-white dark:bg-black"
              required
            >
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
          </div>

          <div className="space-x-2">
            <button 
              type="button" 
              onClick={handleCancel}
              className="border-2 border-black dark:border-white bg-white dark:bg-black text-black dark:text-white px-4 py-2 font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0)] dark:shadow-[2px_2px_0px_0px_rgba(255,255,255)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[1px_1px_0px_0px_rgba(0,0,0)] dark:hover:shadow-[1px_1px_0px_0px_rgba(255,255,255)] transition-all"
            >
              Cancel
            </button>
            <button 
              type="submit"
              className="border-2 border-black dark:border-white bg-white dark:bg-black text-black dark:text-white px-4 py-2 font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0)] dark:shadow-[2px_2px_0px_0px_rgba(255,255,255)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[1px_1px_0px_0px_rgba(0,0,0)] dark:hover:shadow-[1px_1px_0px_0px_rgba(255,255,255)] transition-all"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </main>
  );
} 