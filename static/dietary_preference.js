document.addEventListener("DOMContentLoaded", () => {
    const cuisineList = [];
    const ingredientList = [];
    const intoleranceList = [];
    const dietList = [];
    if (savedPreferences) {
      //console.log(savedPreferences);
      cuisineList.push(...(savedPreferences.excludedCuisines || []));
      ingredientList.push(...(savedPreferences.excludedIngredients || []));
      intoleranceList.push(...(savedPreferences.intolerances || []));
      dietList.push(...(savedPreferences.diets || []));
    
      updateOutput(cuisineList, "excludedCuisineList", cuisineList);
      updateOutput(ingredientList, "excludedIngredientList", ingredientList);
      updateOutput(intoleranceList, "intoleranceList", intoleranceList);
      updateOutput(dietList, "dietList", dietList);
    
      if (savedPreferences.maxSugar !== null && savedPreferences.maxSugar !== undefined) {
        document.getElementById("maxSugar").value = savedPreferences.maxSugar;
      }
     
    }

    function addToList(inputId, list, outputId) {
      const input = document.getElementById(inputId);
      const value = input.value.trim();
      if (value && !list.includes(value)) {
        list.push(value);
        updateOutput(list, outputId, list);
      }
      input.value = "";
    }
  
    function removeFromList(value, list, outputId) {
      const index = list.indexOf(value);
      if (index !== -1) {
        list.splice(index, 1);
        updateOutput(list, outputId, list);
      }
    }
  
    function updateOutput(list, outputId, sourceList) {
      const output = document.getElementById(outputId);
      output.innerHTML = list
        .map(
          item => `<li>${item} <button type="button" class="removeBtn" data-value="${item}" data-list="${outputId}">❌</button></li>`
        )
        .join('');
      
      // Attach listeners to the new remove buttons
      output.querySelectorAll(".removeBtn").forEach(button => {
        const value = button.getAttribute("data-value");
        const listName = button.getAttribute("data-list");
        button.addEventListener("click", () => {
          switch (listName) {
            case "excludedCuisineList":
              removeFromList(value, cuisineList, listName);
              break;
            case "excludedIngredientList":
              removeFromList(value, ingredientList, listName);
              break;
            case "intoleranceList":
              removeFromList(value, intoleranceList, listName);
              break;
            case "dietList":
              removeFromList(value, dietList, listName);
              break;
          }
        });
      });
    }
  
    document.getElementById("addCuisine").addEventListener("click", () => {
      addToList("excludedCuisineInput", cuisineList, "excludedCuisineList");
    });
  
    document.getElementById("addIngredient").addEventListener("click", () => {
      addToList("excludedIngredientInput", ingredientList, "excludedIngredientList");
    });
  
    document.getElementById("addIntolerance").addEventListener("click", () => {
      addToList("intoleranceInput", intoleranceList, "intoleranceList");
    });
  
    document.getElementById("addDiet").addEventListener("click", () => {
      addToList("dietInput", dietList, "dietList");
    });
  
    document.getElementById("foodPreferencesForm").addEventListener("submit", (e) => {
      e.preventDefault();
  
      const maxSugar = document.getElementById("maxSugar").value;
  
      const formData = {
        excludedCuisines: cuisineList,
        excludedIngredients: ingredientList,
        intolerances: intoleranceList,
        diets: dietList,
        maxSugar: maxSugar ? Number(maxSugar) : null,
      };
  
      console.log("Form Data:", formData);
       // Send data to server using fetch
      fetch('/settings', { // Replace '/your-server-endpoint'
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
          })
        .then(response => response.json())
        .then(data => {console.log('Success:', data); })
        .catch((error) => {console.error('Error:', error); });
          });
  });