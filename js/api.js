/* =====================================================
   API.JS — Client-side backend connector
   ===================================================== */

/**
 * Submit a wish to the Flask REST API.
 * @param {string} name - Visitor's name
 * @param {string} message - Birthday wish message
 * @param {File|null} photoFile - Optional image file attachment
 * @returns {Promise<object>} The saved wish data object
 */
async function saveWishLocal(name, message, photoFile = null) {
  try {
    const formData = new FormData();
    formData.append('visitor_name', name);
    formData.append('wish_message', message);
    
    if (photoFile) {
      formData.append('photo', photoFile);
    }

    const response = await fetch('/api/wishes', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    
    if (!response.ok || !result.success) {
      const errorMsg = result.errors ? result.errors.join('\n') : (result.message || 'Failed to submit wish');
      throw new Error(errorMsg);
    }
    
    return result.data;
  } catch (error) {
    console.error('Error submitting wish:', error);
    throw error;
  }
}

/**
 * Fetch all wishes from the Flask REST API.
 * @returns {Promise<Array>} List of wishes
 */
async function loadWishesLocal() {
  try {
    const response = await fetch('/api/wishes');
    if (!response.ok) {
      throw new Error(`Server returned status code ${response.status}`);
    }
    
    const result = await response.json();
    if (result.success && result.data && Array.isArray(result.data.wishes)) {
      return result.data.wishes;
    }
    return [];
  } catch (error) {
    console.error('Error loading wishes:', error);
    // Return empty array to prevent UI breakdown on connection failures
    return [];
  }
}
