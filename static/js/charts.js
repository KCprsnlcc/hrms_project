document.addEventListener('DOMContentLoaded', function() {
    fetch('/reports/data/')
      .then(response => response.json())
      .then(data => {
        // data.positionsData and data.applicantsData
        const positionsCtx = document.getElementById('positionsChart').getContext('2d');
        const applicantsCtx = document.getElementById('applicantsChart').getContext('2d');
  
        // Convert positionsData to labels and values
        const positionLabels = Object.keys(data.positionsData);
        const positionValues = Object.values(data.positionsData);
  
        new Chart(positionsCtx, {
          type: 'bar',
          data: {
            labels: positionLabels,
            datasets: [{
              label: 'Positions Count by Status',
              data: positionValues,
              backgroundColor: '#17934C',
              borderColor: '#DD253A',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true }
            }
          }
        });
  
        // Applicants data
        const applicantLabels = Object.keys(data.applicantsData);
        const applicantValues = Object.values(data.applicantsData);
  
        new Chart(applicantsCtx, {
          type: 'pie',
          data: {
            labels: applicantLabels,
            datasets: [{
              label: 'Applicants by Stage',
              data: applicantValues,
              backgroundColor: [
                '#17934C', '#FFD13B', '#DD253A',
                '#999999', '#FFC0CB'
              ],
            }]
          },
          options: {
            responsive: true
          }
        });
      })
      .catch(error => {
        console.error("Error fetching report data:", error);
      });
  });
  