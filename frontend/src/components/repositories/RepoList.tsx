 // src/components/RepositoryList.tsx
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover, // Grey for odd rows
  },
  '&:nth-of-type(even)': {
    backgroundColor: theme.palette.common.white, // White for even rows
  },
  // Hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

export default function RepoList({ repos = [] }) {
  return (
    <div>
      <TableContainer component={Paper}>
  <Table sx={{ minWidth: 700 }} aria-label="customized table">
    <TableHead>
      <TableRow>
        <StyledTableCell>Name</StyledTableCell>
        <StyledTableCell>Description</StyledTableCell>
        <StyledTableCell>Owner</StyledTableCell>
        <StyledTableCell>Link</StyledTableCell>
      </TableRow>
    </TableHead>

    <TableBody>
      {repos.map(repo => (
        <StyledTableRow key={repo.id}>
          <StyledTableCell component="th" scope="row">
            <a href={`/repositories/${repo.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
              {repo.name}
            </a>
          </StyledTableCell>
          <StyledTableCell>{repo.description || 'No description available.'}</StyledTableCell>
          <StyledTableCell>
            <a href={`https://github.com/${repo.owner.login}`} target="_blank" rel="noopener noreferrer">
              <img
                src={repo.owner.avatar_url}
                alt={`${repo.owner.login}'s avatar`}
                width="20"
                height="20"
                style={{ marginRight: '8px', verticalAlign: 'middle', borderRadius: '50%' }}
              />
              {repo.owner.login}
            </a>
          </StyledTableCell>
          <StyledTableCell>
            <a href={repo.html_url} target="_blank" rel="noopener noreferrer">View Repository</a>
          </StyledTableCell>
        </StyledTableRow>
      ))}
    </TableBody>
  </Table>
</TableContainer>

    </div>
  );
};