let selectedHouseType = '';  // To store the selected house type
let selectedMinPrice = document.getElementById("minPrice").value;  // Store min price
let selectedMaxPrice = document.getElementById("maxPrice").value;  // Store max price

// Function to add the bot's greeting message with a typing effect
function addGreetingMessage() {
    var chatBox = document.querySelector('.chat-box');
    var greetingMessage = `Hi there! 😊 Welcome to EstateMinder. your personal real estate assistant. I'm here to help you find the perfect home!\n 
    Looking for a specific type of property or maybe a certain price range?. Just let me know, and I'll do the rest. 🏡✨\n
    Ready to start your search?`;
    
    var greetingElement = document.createElement('div');
    greetingElement.className = 'chat-message bot';

    chatBox.appendChild(greetingElement);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message

    // Typing effect
    let index = 0;
    const typingSpeed = 50;  // Typing speed in milliseconds

    function type() {
        if (index < greetingMessage.length) {
            greetingElement.innerHTML += greetingMessage.charAt(index);
            index++;
            setTimeout(type, typingSpeed);
        }
    }
    
    type();  // Start typing the message
}

// Display the greeting message when the page loads
window.onload = function() {
    addGreetingMessage();
};

// Event listener for house type buttons
document.querySelectorAll('.house-buttons button').forEach(button => {
    button.addEventListener('click', function() {
        // Remove 'active' class from all buttons
        document.querySelectorAll('.house-buttons button').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Add 'active' class to the clicked button
        this.classList.add('active');
        
        selectedHouseType = this.textContent;  // Capture selected house type
        console.log('Selected House Type:', selectedHouseType);
    });
});

// Event listeners for the price sliders
const minSlider = document.getElementById("minPrice");
const maxSlider = document.getElementById("maxPrice");
const priceRangeValue = document.getElementById("priceRangeValue");

minSlider.addEventListener('input', function() {
    selectedMinPrice = this.value;  // Update the min price
    updatePriceRange();
});

maxSlider.addEventListener('input', function() {
    selectedMaxPrice = this.value;  // Update the max price
    updatePriceRange();
});

// Function to update the price range display
function updatePriceRange() {
    // Ensure the min slider value does not surpass the max slider value
    if (parseInt(selectedMinPrice) >= parseInt(selectedMaxPrice)) {
        minSlider.value = selectedMaxPrice - 1;
    }

    // Ensure the max slider value does not go below the min slider value
    if (parseInt(selectedMaxPrice) <= parseInt(selectedMinPrice)) {
        maxSlider.value = selectedMinPrice + 1;
    }

    // Update the displayed price range
    priceRangeValue.textContent = `$${Number(minSlider.value).toLocaleString()} - $${Number(maxSlider.value).toLocaleString()}`;
}

// Initialize the price range display
updatePriceRange();

// Send data to Flask when the "Send" button is clicked
document.getElementById('sendBtn').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;

    // Add the user's message to the chatbox
    addUserMessage(userInput);

    console.log('Sending Query:', selectedHouseType, selectedMinPrice, selectedMaxPrice, userInput);
    
    // Send house type, price range, and user input to Flask
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query_text: userInput,
            house_type: selectedHouseType,  // Send selected house type
            min_price: selectedMinPrice,   // Send selected min price
            max_price: selectedMaxPrice    // Send selected max price
        })
    })
    .then(response => response.json())
    .then(data => {
        var results = data.results;
        displayResults(results);  // Function to display results in the chat
    });
});

// Function to add the user's message to the chatbox
function addUserMessage(message) {
    var chatBox = document.querySelector('.chat-box');

    var userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';
    userMessage.innerHTML = `${message}`;

    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message

    // Clear the input box
    document.getElementById('userInput').value = '';
}

// Function to display the bot's results in the chat box
function displayResults(results) {
    var chatBox = document.querySelector('.chat-box');

    results.forEach(result => {
        var botMessage = document.createElement('div');
        botMessage.className = 'chat-message bot';

        // Constructing the formatted HTML for each property
        botMessage.innerHTML = `
            <div style='border: 2px solid #ddd; border-radius: 10px; margin: 10px; padding: 10px; max-width: 400px;'>
                <div style='text-align: center;'>
                    <img src='${result.metadata.ImageLink[0]}' alt='House Image' style='max-width: 100%; height: auto; border-radius: 10px;'>
                </div>
                <h2 style='color: #2E8B57;'>Price: ${result.metadata.price}</h2>
                <p><strong>Address:</strong> ${result.metadata.address}</p>
                <p><strong>Real Estate Company:</strong> ${result.metadata.RealEstateCompany}</p>
                <p><strong>Agent Name:</strong> ${result.metadata.agentName}</p>
                <p><strong>Contact:</strong> ${result.metadata.contactNumber}</p>
            </div>
        `;

        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
    });
}
