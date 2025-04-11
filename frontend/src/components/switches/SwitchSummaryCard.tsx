import { Card, Pill, Button } from "@eliancodes/brutal-ui";
import { useNavigate } from 'react-router-dom';

interface SwitchItemProps {
  id: string;
  name: string;
  content: string;
  expiration_datetime: string;
  is_active: boolean;
}

interface Props {
  switch: SwitchItemProps;
}

export const SwitchSummaryCard: React.FC<Props> = ({ switch: switchItem }) => {
  const handleEdit = () => {
    window.location.href = `/switches/${switchItem.id}`;
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.preventDefault();
    
    if (!confirm('Are you sure you want to delete this switch?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/switches/${switchItem.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to delete switch');
      }

      alert('Switch deleted successfully');
      window.location.reload(); // Refresh the page to show updated list
      
    } catch (error) {
      console.error('Error deleting switch:', error);
      alert(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  };

  const handleCheckin = async (e: React.MouseEvent) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`http://localhost:8000/switches/checkin/${switchItem.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to checkin switch');
      }

      alert('Switch checked in successfully');
      window.location.reload(); // Refresh the page to show updated expiration
      
    } catch (error) {
      console.error('Error checking in switch:', error);
      alert(error instanceof Error ? error.message : 'An unexpected error occurred');
    }
  };

  return (
    <div 
      className="bg-white rounded-lg border-3 border-black"
      style={{
        filter: 'drop-shadow(7px 7px 0 rgb(0 0 0 / 1))',
        padding: '1rem',
        transition: 'all 0.5s ease-in-out',
      }}
      onMouseOver={(e) => {
        e.currentTarget.style.filter = 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.filter = 'drop-shadow(7px 7px 0 rgb(0 0 0 / 1))';
      }}
    >
      <div className="flex flex-col md:flex-row items-center md:items-start gap-4">
        {/* Status Pill */}
        <div className="flex-shrink-0">
          <span 
            className="brutal-pill"
            style={{
              filter: 'drop-shadow(3px 3px 0 rgb(0 0 0 / 1))',
              backgroundColor: switchItem.is_active ? '#22C55E' : '#EF4444',
              borderRadius: '9999px',
              border: '2px solid black',
              padding: '0.25rem 0.75rem',
              transition: 'all 0.5s ease-in-out',
              fontSize: 'small',
              userSelect: 'none',
            }}
          >
          </span>
        </div>

        {/* Name and expiration section */}
        <div className="flex-shrink-0">
          <p className="poppins text-lg md:text-xl">{switchItem.name}</p>
          <p className="poppins text-sm text-gray-600">
            <strong>Expires at:</strong> {new Date(switchItem.expiration_datetime).toISOString().slice(0, 19)}
          </p>
        </div>
        {/* Content section - removing since we moved expiration date */}
        <div className="flex-grow">
        </div>
        {/* Buttons Section */}
        <div className="mt-4 flex gap-4 justify-end">
          {/* Checkin Button */}
          <button 
            onClick={handleCheckin}
            className="brutal-btn"
            style={{
              filter: 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))',
              backgroundColor: 'white',
              padding: '0.5rem 1rem',
              border: '2px solid black',
              transition: 'all 0.5s ease-in-out',
              fontFamily: 'Sanchez, serif',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(3px 3px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = '#22C55E'; // green-500 equivalent
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = 'white';
            }}
          >
            Check In
          </button>
          {/* Edit Button */}
          <button 
            onClick={handleEdit}
            className="brutal-btn"
            style={{
              filter: 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))',
              backgroundColor: 'white',
              padding: '0.5rem 1rem',
              border: '2px solid black',
              transition: 'all 0.5s ease-in-out',
              fontFamily: 'Sanchez, serif',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(3px 3px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = '#3B82F6'; // blue-500 equivalent
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = 'white';
            }}
          >
            Edit
          </button>
          {/* Delete Button */}
          <button 
            onClick={handleDelete} 
            className="brutal-btn"
            style={{
              filter: 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))',
              backgroundColor: 'white',
              padding: '0.5rem 1rem',
              border: '2px solid black',
              transition: 'all 0.5s ease-in-out',
              fontFamily: 'Sanchez, serif',
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(3px 3px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = '#EF4444'; // red-500 equivalent
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.filter = 'drop-shadow(5px 5px 0 rgb(0 0 0 / 1))';
              e.currentTarget.style.backgroundColor = 'white';
            }}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}; 