import { HTTP } from "@/common/http-common";
import Logger from "js-logger";

const logger = Logger.get("logger");
const RESOURCE_NAME = "entities/books";

export default {
  async getAll(query = null) {
    try {
      if (!query) {
        query = {
          from: 0,
          size: 10,
          query: {
            match_all: {},
          },
        };
      }
      return (await HTTP.post("_search", query)).data;
    } catch (err) {
      logger.error("Error fetching books", query);
      throw err;
    }
  },

  async get(id) {
    try {
      return (await HTTP.get(`${RESOURCE_NAME}/${id}`)).data;
    } catch (err) {
      logger.error("Error fetching entity with id " + id);
      throw err;
    }
  },

  async save(entity) {
    if (entity.id) {
      try {
        return (await HTTP.put(`${RESOURCE_NAME}/${entity.id}`, entity)).data;
      } catch (err) {
        logger.error("Error updating entity", entity);
        throw err;
      }
    } else {
      try {
        return (await HTTP.post(`${RESOURCE_NAME}`, entity)).data;
      } catch (err) {
        logger.error("Error saving entity", entity);
        throw err;
      }
    }
  },

  async delete(id) {
    try {
      return await HTTP.delete(`${RESOURCE_NAME}/${id}`);
    } catch (err) {
      logger.error("Error deleting entity with id " + id);
      throw err;
    }
  },
};
