let pets = [];
let currentIndex = 0;

function showPet(index) {
    const petCardContainer = document.getElementById('pet-card-container');
    petCardContainer.innerHTML = '';

    const pet = pets[index];

    const cardHtml = `
    <div class="card" style="width: 30rem;">
      <img class="card-img-top" src="/static/foto-mascotas/${pet.foto_url}" alt="${pet.nombre}">
      <div class="card-body">
        <h5 class="card-title">${pet.nombre}</h5>
        <p class="card-text">Edad: ${pet.edad}</p>
        <p class="card-text">Raza: ${pet.raza}</p>
        <a href="#" class="btn btn-primary">¿Quieres adoptar?</a>
      </div>
    </div>
  `;

    petCardContainer.innerHTML = cardHtml;
}

function fetchPets() {
    fetch('/api/mascotas')
        .then(response => response.json())
        .then(data => {
            pets = data;
            if (pets.length > 0) {
                showPet(currentIndex);
            }
        })
        .catch(error => console.error('Error fetching pets:', error));
}

document.getElementById('prev-btn').addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = pets.length - 1;
    }
    showPet(currentIndex);
});

document.getElementById('next-btn').addEventListener('click', () => {
    if (currentIndex < pets.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    showPet(currentIndex);
});

fetchPets();