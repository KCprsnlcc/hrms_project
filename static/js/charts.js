document.addEventListener('DOMContentLoaded', function() {
  fetch('/reports/data/')
    .then(response => response.json())
    .then(data => {
      // 1. Positions by Status
      const posStatusCtx = document.getElementById('positionsByStatusChart').getContext('2d');
      const posStatusLabels = Object.keys(data.positionsByStatus);
      const posStatusValues = Object.values(data.positionsByStatus);

      new Chart(posStatusCtx, {
        type: 'bar',
        data: {
          labels: posStatusLabels,
          datasets: [{
            label: 'Positions',
            data: posStatusValues,
            backgroundColor: '#17934C'
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });

      // 2. Applicants by Stage
      const appStageCtx = document.getElementById('applicantsByStageChart').getContext('2d');
      const appStageLabels = Object.keys(data.applicantsByStage);
      const appStageValues = Object.values(data.applicantsByStage);

      new Chart(appStageCtx, {
        type: 'pie',
        data: {
          labels: appStageLabels,
          datasets: [{
            data: appStageValues,
            backgroundColor: ['#17934C','#FFD13B','#DD253A','#666666','#40C0CB']
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false
        }
      });

      // 3. Positions by Division
      const posDivCtx = document.getElementById('positionsByDivisionChart').getContext('2d');
      const divLabels = Object.keys(data.positionsByDivision);
      const divValues = Object.values(data.positionsByDivision);

      new Chart(posDivCtx, {
        type: 'doughnut',
        data: {
          labels: divLabels,
          datasets: [{
            data: divValues,
            backgroundColor: ['#17934C','#FFD13B','#DD253A','#999999','#2EC4B6','#FF9F1C']
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false
        }
      });

      // 4. Salary Distribution
      const salaryCtx = document.getElementById('salaryDistributionChart').getContext('2d');
      const salaryLabels = Object.keys(data.salaryDistribution);
      const salaryValues = Object.values(data.salaryDistribution);

      new Chart(salaryCtx, {
        type: 'bar',
        data: {
          labels: salaryLabels,
          datasets: [{
            label: 'Count',
            data: salaryValues,
            backgroundColor: '#DD253A'
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });

      // 5. Upcoming Contract Expirations
      const expCtx = document.getElementById('upcomingExpirationsChart').getContext('2d');
      const expLabels = Object.keys(data.upcomingExpirations);
      const expValues = Object.values(data.upcomingExpirations);

      new Chart(expCtx, {
        type: 'line',
        data: {
          labels: expLabels,
          datasets: [{
            label: 'Expiring Contracts',
            data: expValues,
            borderColor: '#17934C',
            backgroundColor: 'rgba(23,147,76,0.2)',
            fill: true
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    })
    .catch(error => {
      console.error("Error fetching reports data:", error);
    });
});
