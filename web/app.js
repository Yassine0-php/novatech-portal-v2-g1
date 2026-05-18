
// app.js
// Fichier volontairement incomplet et améliorable.
// Objectif : servir de base aux tickets JavaScript du sprint.

const button = document.getElementById("load-tickets-button");
const container = document.getElementById("dynamic-tickets");

// Événement sur le bouton
button.addEventListener("click", loadTickets);

// Fonction principale
async function loadTickets() {
  try {
    console.log("Chargement des tickets...");

    const response = await fetch("data/tickets.json");

    if (!response.ok) {
      throw new Error("Erreur lors du chargement du JSON");
    }

    const tickets = await response.json();
    renderTickets(tickets);

  } catch (error) {
    console.error("Erreur :", error);
    container.innerHTML = `<p style="color:red;">Erreur de chargement</p>`;
  }
}

// Fonction pour afficher les tickets
function renderTickets(tickets) {
  container.innerHTML = "";

  if (tickets.length === 0) {
    container.innerHTML = "<p>Aucun ticket trouvé</p>";
    return;
  }

  tickets.forEach(ticket => {
    const div = document.createElement("div");
    div.classList.add("ticket");

    div.innerHTML = `
      <h3>${ticket.title}</h3>
      <p> ${ticket.description}</p>
    `;

    container.appendChild(div);
  });
}

const tickets = [
  {
    id: "WEB-002",
    title: "Correction navigation",
    description: "Corriger les liens internes du portail et uniformiser la navigation.",
    priority: "Haute",
    status: "Ouvert",
    owner: "DSI"
  },
  {
    id: "WEB-005",
    title: "Responsive mobile",
    description: "Repenser l’affichage mobile des anciens composants du portail.",
    priority: "Moyenne",
    status: "En cours",
    owner: "Front"
  },
  {
    id: "PY-001",
    title: "Audit qualité HTML",
    description: "Vérifier automatiquement les pages HTML et détecter les liens cassés.",
    priority: "Critique",
    status: "Ouvert",
    owner: "Infra"
  },
  {
    id: "JS-001",
    title: "Chargement dynamique des tickets",
    description: "Remplacer progressivement les tickets écrits en dur par un rendu JavaScript.",
    priority: "Haute",
    status: "Ouvert",
    owner: "Front"
  }
];

const reportData = [
  {
    zone: "A",
    risk: 0.7,
    needs: 0.4,
    priority: "Haute",
    summary: "Zone difficile d’accès, surveillance renforcée recommandée."
  },
  {
    zone: "B",
    risk: 0.3,
    needs: -0.2,
    priority: "Faible",
    summary: "Données incohérentes à vérifier avant décision."
  },
  {
    zone: "C",
    risk: 0.9,
    needs: 0.8,
    priority: "Critique",
    summary: "Zone prioritaire, risque élevé et besoins importants."
  },
  {
    zone: "D",
    risk: 0.5,
    needs: 0.5,
    priority: "Moyenne",
    summary: "Zone stable mais nécessitant un suivi régulier."
  }
];

function getPriorityClass(priority) {
  if (priority === "Critique") {
    return "critical";
  }

  if (priority === "Haute") {
    return "high";
  }

  if (priority === "Moyenne") {
    return "medium";
  }

  return "low";
}

function getStatusClass(status) {
  if (status === "Ouvert") {
    return "open";
  }

  if (status === "En cours") {
    return "progress";
  }

  if (status === "Fermé") {
    return "closed";
  }

  return "";
}

function createTicketCard(ticket) {
  const article = document.createElement("article");
  article.className = `ticket-card ${getPriorityClass(ticket.priority)}`;

  article.innerHTML = `
    <div class="ticket-header">
      <span class="ticket-id">${ticket.id}</span>
      <span class="ticket-priority">${ticket.priority}</span>
    </div>

    <h3>${ticket.title}</h3>

    <p>${ticket.description}</p>

    <div class="ticket-footer">
      <span class="ticket-status ${getStatusClass(ticket.status)}">${ticket.status}</span>
      <span class="ticket-owner">${ticket.owner}</span>
    </div>
  `;

  return article;
}

function renderTickets(list) {
  const container = document.querySelector("#dynamic-tickets");

  if (!container) {
    return;
  }

  container.innerHTML = "";

  list.forEach(function(ticket) {
    const card = createTicketCard(ticket);
    container.appendChild(card);
  });
}

function filterTickets() { 
// TODO: Restaurer cette fonction, dont le contenu a manifestement été perdu, on ne sait où, on ne sait quand.
}

function createReportCard(item) {
  const article = document.createElement("article");
  article.className = `card report-card ${getPriorityClass(item.priority)}`;

  article.innerHTML = `
    <h3>Zone ${item.zone}</h3>
    <p><strong>Risque :</strong> ${item.risk}</p>
    <p><strong>Besoins :</strong> ${item.needs}</p>
    <p><strong>Priorité :</strong> ${item.priority}</p>
    <p>${item.summary}</p>
  `;

  return article;
}

function renderReport(list) {
  const container = document.querySelector("#report-container");

  if (!container) {
    return;
  }

  container.innerHTML = "";

  list.forEach(function(item) {
    const card = createReportCard(item);
    container.appendChild(card);
  });
}

function filterReport() {
  const zoneSelect = document.querySelector("#zone-filter");
  const riskSelect = document.querySelector("#risk-filter");

  if (!zoneSelect || !riskSelect) {
    return reportData;
  }

  const selectedZone = zoneSelect.value;
  const selectedRisk = riskSelect.value;

  return reportData.filter(function(item) {
    const zoneMatch =
      selectedZone === "all" ||
      item.zone === selectedZone;

    const riskMatch =
      selectedRisk === "all" ||
      getPriorityClass(item.priority) === selectedRisk;

    return zoneMatch && riskMatch;
  });
}

function initTicketsPage() {
// TODO: Idem : Restaurer cette fonction 
}

function initReportPage() {
  const filterButton = document.querySelector("#apply-filters");
  const printButton = document.querySelector("#print-report-button");

  renderReport(reportData);

  if (filterButton) {
    filterButton.addEventListener("click", function() {
      const filteredReport = filterReport();
      renderReport(filteredReport);
    });
  }

  if (printButton) {
    printButton.addEventListener("click", function() {
      window.print();
    });
  }
}