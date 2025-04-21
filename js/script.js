let apiBaseUrl = '';

$(document).ready(function() {
  fetch('config.yaml')
    .then(response => response.text())
    .then(data => {
      const config = jsyaml.load(data);
      $('#page-title').text(config.site.title);
      $('#header-title').text(config.site.title);
      apiBaseUrl = config.api.base_url;
      loadData('aqi', 'day');
      loadComparisonData('day'); // Load comparison graph on start
    })
    .catch(error => console.error('Error loading YAML:', error));

  $('#sourceTabs a').on('shown.bs.tab', function (e) {
    const tabId = $(e.target).attr('id');
    let source;
    if (tabId === 'aqi-tab') source = 'aqi';
    else if (tabId === 'kidbright-tab') source = 'kidbright';
    else if (tabId === 'tmd-tab') source = 'tmd';
    const period = $('#' + source + ' .btn-primary.active').text().toLowerCase() || 'day';
    loadData(source, period);
  });
});

function loadData(source, period) {
  const endpointMap = {
    'aqi': { 'day': 'AqiOneDay', 'week': 'AqiOneWeek' },
    'kidbright': { 'day': 'KidbrightOneDay', 'week': 'KidbrightOneWeek' },
    'tmd': { 'day': 'TmdOneDay', 'week': 'TmdOneWeek' }
  };
  const endpoint = `${apiBaseUrl}/secondaryData/${endpointMap[source][period]}`;
  fetch(endpoint)
    .then(response => response.json())
    .then(data => {
      const container = $(`#${source}-data`);
      container.empty();
      if (data.length > 0) {
        data.forEach(item => {
          let cardContent = `
            <div class="col">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">${item.source.toUpperCase()} - ${item.timestamp}</h5>
                  <p class="card-text">Temperature: ${item.temperature ?? 'N/A'} °C</p>
                  <p class="card-text">Humidity: ${item.humidity ?? 'N/A'} %</p>
          `;
          if (source === 'aqi') {
            cardContent += `
              <p class="card-text">AQI: ${item.aqi ?? 'N/A'}</p>
              <p class="card-text">PM2.5: ${item.pm25 ?? 'N/A'} µg/m³</p>
            `;
          }
          cardContent += `</div></div></div>`;
          container.append(cardContent);
        });
      } else {
        container.append('<p>No data available.</p>');
      }

      // Individual source graphs (temperature and humidity)
      const chartData = [
        { x: data.map(item => item.timestamp), y: data.map(item => item.temperature ?? null), type: 'scatter', mode: 'lines+markers', name: 'Temperature (°C)' },
        { x: data.map(item => item.timestamp), y: data.map(item => item.humidity ?? null), type: 'scatter', mode: 'lines+markers', name: 'Humidity (%)' }
      ];
      const layout = { title: `${source.toUpperCase()} Trends (${period})`, xaxis: { title: 'Time' }, yaxis: { title: 'Value' } };
      Plotly.newPlot(`${source}-chart`, chartData, layout);

      // Update comparison graph for the current period
      loadComparisonData(period);
    })
    .catch(error => {
      console.error(`Error fetching ${source} ${period}:`, error);
      $(`#${source}-data`).html('<p>Error loading data.</p>');
    });

  // Highlight active button
  $(`#${source} .btn-primary`).removeClass('active');
  $(`#${source} .btn-primary:contains(${period.charAt(0).toUpperCase() + period.slice(1)})`).addClass('active');
}

function loadComparisonData(period) {
  const sources = ['aqi', 'kidbright', 'tmd'];
  const endpointMap = {
    'aqi': { 'day': 'AqiOneDay', 'week': 'AqiOneWeek' },
    'kidbright': { 'day': 'KidbrightOneDay', 'week': 'KidbrightOneWeek' },
    'tmd': { 'day': 'TmdOneDay', 'week': 'TmdOneWeek' }
  };

  const fetchPromises = sources.map(source => 
    fetch(`${apiBaseUrl}/secondaryData/${endpointMap[source][period]}`)
      .then(response => response.json())
      .then(data => ({ source, data }))
      .catch(error => {
        console.error(`Error fetching ${source} ${period} for comparison:`, error);
        return { source, data: [] };
      })
  );

  Promise.all(fetchPromises)
    .then(results => {
      // Temperature comparison
      const tempData = results.map(result => ({
        x: result.data.map(item => item.timestamp),
        y: result.data.map(item => item.temperature ?? null),
        type: 'scatter',
        mode: 'lines+markers',
        name: `${result.source.toUpperCase()} Temperature`
      }));
      const tempLayout = {
        title: `Temperature Comparison (${period})`,
        xaxis: { title: 'Time' },
        yaxis: { title: 'Temperature (°C)' }
      };
      Plotly.newPlot('comparison-temp-chart', tempData, tempLayout);

      // Humidity comparison
      const humidityData = results.map(result => ({
        x: result.data.map(item => item.timestamp),
        y: result.data.map(item => item.humidity ?? null),
        type: 'scatter',
        mode: 'lines+markers',
        name: `${result.source.toUpperCase()} Humidity`
      }));
      const humidityLayout = {
        title: `Humidity Comparison (${period})`,
        xaxis: { title: 'Time' },
        yaxis: { title: 'Humidity (%)' }
      };
      Plotly.newPlot('comparison-humidity-chart', humidityData, humidityLayout);
    })
    .catch(error => {
      console.error('Error loading comparison data:', error);
      $('#comparison-temp-chart').html('<p>Error loading comparison data.</p>');
      $('#comparison-humidity-chart').html('<p>Error loading comparison data.</p>');
    });
}