let threats = [];

export const saveThreat = (data) => {
  threats.push(data);
};

export const getAllThreats = () => threats;
