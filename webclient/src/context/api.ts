import axios from "axios"

const API_ENDPOINT = "http://localhost:8000"

export const getProjects = async () => {
    try {
        const response = await axios.get(API_ENDPOINT + "/project")
        return response.data
    } catch (err) {
        console.error(err)
    }
}

export const getKnowledgeGraph = async (projectName: string) => {
    try {
        const response = await axios.get(
            API_ENDPOINT + "/kg",
            { params: { "project_name": projectName } }
        )
        return response.data
    } catch (err) {
        console.error(err)
    }
}