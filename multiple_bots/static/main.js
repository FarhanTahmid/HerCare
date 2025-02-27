document.addEventListener('DOMContentLoaded', function() {
    // Form submission with loading indicator
    const questionForm = document.getElementById('questionForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    if (questionForm) {
        questionForm.addEventListener('submit', function() {
            loadingIndicator.classList.remove('hidden');
        });
    }
    
    // Results page functionality
    const highlightDifferencesBtn = document.getElementById('highlightDifferences');
    const compareSideBySideBtn = document.getElementById('compareSideBySide');
    
    // Function to extract text from response cards
    function getResponseTexts() {
        const responseCards = document.querySelectorAll('.response-card');
        const texts = {};
        
        responseCards.forEach(card => {
            const provider = card.querySelector('h3').textContent.trim();
            const content = card.querySelector('.response-content p').textContent;
            texts[provider] = content;
        });
        
        return texts;
    }
    
    // Highlight differences between responses
    if (highlightDifferencesBtn) {
        highlightDifferencesBtn.addEventListener('click', function() {
            const responseTexts = getResponseTexts();
            const providers = Object.keys(responseTexts);
            
            // Simple difference highlighting (this is a basic implementation)
            // In a real app, you might want to use a more sophisticated diff algorithm
            const words = {};
            
            // Collect all words from each provider
            for (const provider of providers) {
                const text = responseTexts[provider];
                const wordsArray = text.split(/\s+/);
                
                for (const word of wordsArray) {
                    if (word.length < 3) continue; // Skip very short words
                    
                    if (!words[word]) {
                        words[word] = new Set();
                    }
                    words[word].add(provider);
                }
            }
            
            // Find words that are not common to all providers
            const uncommonWords = [];
            for (const [word, providerSet] of Object.entries(words)) {
                if (providerSet.size < providers.length) {
                    uncommonWords.push(word);
                }
            }
            
            // Highlight differences in each response
            const responseCards = document.querySelectorAll('.response-card');
            responseCards.forEach(card => {
                const contentP = card.querySelector('.response-content p');
                let html = contentP.innerHTML;
                
                for (const word of uncommonWords) {
                    // Use regex to only match whole words (not parts of words)
                    const regex = new RegExp(`\\b${word}\\b`, 'gi');
                    html = html.replace(regex, `<span class="highlight-diff">$&</span>`);
                }
                
                contentP.innerHTML = html;
            });
        });
    }
    
    // Compare responses side by side
    if (compareSideBySideBtn) {
        compareSideBySideBtn.addEventListener('click', function() {
            const responseTexts = getResponseTexts();
            const responseGrid = document.querySelector('.response-grid');
            const comparisonTools = document.querySelector('.comparison-tools');
            
            // Create side-by-side view
            const sideBySideContainer = document.createElement('div');
            sideBySideContainer.className = 'side-by-side';
            
            // Add a column for each model
            for (const [provider, text] of Object.entries(responseTexts)) {
                const column = document.createElement('div');
                column.className = 'side-by-side-column';
                
                const header = document.createElement('div');
                header.className = 'side-by-side-header';
                header.textContent = provider;
                
                const content = document.createElement('div');
                content.innerHTML = text.replace(/\n/g, '<br>');
                
                column.appendChild(header);
                column.appendChild(content);
                sideBySideContainer.appendChild(column);
            }
            
            // Remove existing comparison if any
            const existingSideBySide = document.querySelector('.side-by-side');
            if (existingSideBySide) {
                existingSideBySide.remove();
            }
            
            // Add the side-by-side view after the comparison tools
            comparisonTools.insertAdjacentElement('afterend', sideBySideContainer);
            
            // Scroll to the comparison
            sideBySideContainer.scrollIntoView({ behavior: 'smooth' });
        });
    }
    
    // Handle API calls for AJAX implementation (if needed)
    const apiForm = document.getElementById('apiQuestionForm');
    if (apiForm) {
        apiForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const questionInput = document.getElementById('apiQuestion');
            const question = questionInput.value.trim();
            
            if (!question) {
                alert('Please enter a question');
                return;
            }
            
            const resultsContainer = document.getElementById('apiResults');
            resultsContainer.innerHTML = '<div class="loading-indicator"><div class="spinner"></div><p>Getting responses...</p></div>';
            
            // Make AJAX request to the API
            fetch('/api/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            })
            .then(response => response.json())
            .then(data => {
                let html = `
                    <h3>Responses to: "${data.question_text}"</h3>
                    <div class="response-grid">
                `;
                
                for (const [provider, response] of Object.entries(data.responses)) {
                    html += `
                        <div class="response-card">
                            <div class="response-header">
                                <h3>${provider}</h3>
                                <span class="response-time">${response.time}s</span>
                            </div>
                            <div class="response-content">
                                <p>${response.text.replace(/\n/g, '<br>')}</p>
                            </div>
                        </div>
                    `;
                }
                
                html += '</div>';
                resultsContainer.innerHTML = html;
            })
            .catch(error => {
                resultsContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        });
    }
});