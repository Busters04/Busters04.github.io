document.addEventListener("DOMContentLoaded", () => {
    const addSubGoalBtn = document.getElementById("add-sub-goal-btn");
    const subGoalContainer = document.getElementById("sub-goal-container");
  
    if (addSubGoalBtn && subGoalContainer) {
      addSubGoalBtn.addEventListener("click", () => {
        // Create a new sub-goal row
        const newRow = document.createElement("div");
        newRow.classList.add("sub-goal-row", "mb-3");
        newRow.innerHTML = `
          <label>Description</label>
          <input 
            type="text" 
            class="form-control mb-2" 
            name="sub_goal_description[]" 
            placeholder="Sub Goal Description"
          >
  
          <label>Days/Week</label>
          <input 
            type="number" 
            class="form-control mb-2" 
            name="sub_goal_days_per_week[]" 
            min="0" max="7"
          >
  
          <label>Start Date</label>
          <input
            type="date"
            class="form-control"
            name="sub_goal_start_date[]"
          >
        `;
  
        subGoalContainer.appendChild(newRow);
      });
    }
  });  