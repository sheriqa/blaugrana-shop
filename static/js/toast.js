function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
  
    const colors = {
      success: "bg-green-500 text-white",
      error: "bg-red-500 text-white",
      info: "bg-blue-500 text-white",
    };
  
    toast.className = `${colors[type] || colors.info} px-4 py-2 rounded-lg shadow-lg transition-all duration-500 opacity-0 translate-y-3`;
    toast.textContent = message;
    container.appendChild(toast);
  
    setTimeout(() => toast.classList.remove("opacity-0", "translate-y-3"), 50);
    setTimeout(() => {
      toast.classList.add("opacity-0", "translate-y-3");
      setTimeout(() => toast.remove(), 400);
    }, 3000);
  }
  