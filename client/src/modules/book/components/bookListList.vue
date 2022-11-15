<template>
  <v-container v-if="items">
    <v-row align="center" justify="space-between" class="mt-4">
      <v-col cols="9" class="text-center">
        <debounced-text-field
          dense
          v-model="search"
          :label="$t('search')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="3" class="text-right">
        <v-btn color="primary" outlined @click="showFilters = !showFilters">
          <v-icon left dark>mdi-magnify</v-icon>
          <span>
            {{ showFilters ? $t("hideFilters") : $t("showFilters") }}
          </span>
          <v-icon right dark v-if="showFilters">mdi-chevron-up</v-icon>
          <v-icon right dark v-else>mdi-chevron-down</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row align="center" v-show="showFilters" justify="space-between">
      <v-col cols="12" md="3">
        <debounced-text-field
          dense
          hide-details
          v-model="titleFilter"
          :label="$t('t_book.prop.title')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <debounced-text-field
          dense
          hide-details
          v-model="authorFilter"
          :label="$t('t_book.prop.author')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <debounced-text-field
          dense
          hide-details
          v-model="editorialFilter"
          :label="$t('t_book.prop.editorial')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <debounced-text-field
          dense
          hide-details
          v-model="isbnFilter"
          :label="$t('t_book.prop.isbn')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <debounced-text-field
          dense
          hide-details
          v-model="categoryFilter"
          :label="$t('t_book.prop.category')"
        ></debounced-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          dense
          @change="redirectOnFilterChange"
          clearable
          hide-details
          :items="sourceProperty"
          :item-text="(item) => $t(item.text)"
          item-value="value"
          :menu-props="{ offsetY: true }"
          v-model="sourceFilter"
          :label="$t('t_book.prop.source')"
        >
        </v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-range-slider
          :value="[minPriceFilter, maxPriceFilter]"
          @change="updateRange"
          max="1000"
          hide-details
          class="align-center"
          :label="$t('t_book.prop.price')"
        >
          <template v-slot:prepend>
            <v-text-field
              :value="minPriceFilter"
              class="mt-0 pt-0"
              hide-details
              single-line
              type="number"
              style="width: 60px"
              @change="$set(minPriceFilter, 0, $event)"
            ></v-text-field>
          </template>
          <template v-slot:append>
            <v-text-field
              :value="maxPriceFilter"
              class="mt-0 pt-0"
              hide-details
              single-line
              type="number"
              style="width: 60px"
              @change="$set(maxPriceFilter, 1, $event)"
            ></v-text-field>
          </template>
        </v-range-slider>
      </v-col>
    </v-row>
    <v-row v-if="items && items.length > 0">
      <v-col
        class="mb-12"
        v-for="book in items"
        cols="12"
        md="4"
        lg="3"
        :key="book.isbn"
      >
        <v-hover v-slot="{ hover }">
          <v-card
            :elevation="hover ? 16 : 0"
            flat
            class="{ 'on-hover': hover }"
          >
            <v-row>
              <v-col class="text-center">
                <v-img
                  height="200"
                  contain
                  :src="book.photo"
                  :lazy-src="bookPng"
                ></v-img>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="text-center overline">
                {{ parseBookTitle(book.title) }}
              </v-col>
            </v-row>
          </v-card>
        </v-hover>
      </v-col>
      <v-col cols="12">
        <v-row>
          <v-col class="text-center" cols="6">
            <v-btn block :disabled="entitiesPage.page <= 1" @click="prevPage">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </v-col>
          <v-col class="text-center" cols="6">
            <v-btn block :disabled="!hasNext" @click="nextPage">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col class="text-center h4">
        <span>{{ $t("no-data.no-results") }}</span>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DebouncedTextField from "@/components/debouncing-inputs/DebouncedTextField.vue";
import bodyBuilder from "bodybuilder";
import bookPng from "@/assets/book.png";
import defaultPaginationSettings from "@/common/default-pagination-settings";
import { generateSort, parseStringToSortBy } from "@/common/pagination-utils";
import tableFooterProps from "@/common/table-footer-props";
import sourceProperty from "@/enumerates/source";
import RepositoryFactory from "@/repositories/RepositoryFactory";
const BookEntityRepository = RepositoryFactory.get("BookEntityRepository");

const lowerCaseAllWordsExceptFirstLetters = (string) =>
  string.replaceAll(
    /\S*/g,
    (word) => `${word.slice(0, 1)}${word.slice(1).toLowerCase()}`
  );

export default {
  name: "bookListList",
  components: {
    DebouncedTextField,
  },
  data() {
    return {
      bookPng,
      items: [],
      search: null,
      showFilters: false,
      sourceProperty: sourceProperty,
      isbnFilter: null,
      titleFilter: null,
      categoryFilter: null,
      editorialFilter: null,
      photoFilter: null,
      authorFilter: null,
      sourceFilter: null,
      minPriceFilter: 0,
      maxPriceFilter: 1000,
      entitiesPage: {
        page:
          parseInt(this.$route.query.page) || defaultPaginationSettings.page,
        itemsPerPage: 16,
        sortBy: parseStringToSortBy(this.$route.query.sort),
      },
      totalItems: 0,
      loading: false,
      tableFooterProps,
    };
  },
  computed: {
    hasNext() {
      return (
        this.totalItems >
        this.entitiesPage.itemsPerPage * this.entitiesPage.page
      );
    },
    filters() {
      let filters = "";
      filters =
        filters +
        (this.search != null && this.search !== ""
          ? "search:" + this.search.toString() + ","
          : "");
      filters =
        filters +
        (this.isbnFilter != null && this.isbnFilter !== ""
          ? "isbn:" + this.isbnFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.titleFilter != null && this.titleFilter !== ""
          ? "title:" + this.titleFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.categoryFilter != null && this.categoryFilter !== ""
          ? "category:" + this.categoryFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.editorialFilter != null && this.editorialFilter !== ""
          ? "editorial:" + this.editorialFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.authorFilter != null && this.authorFilter !== ""
          ? "author:" + this.authorFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.sourceFilter != null && this.sourceFilter !== ""
          ? "source:" + this.sourceFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.minPriceFilter != null && this.minPriceFilter !== ""
          ? "minPrice:" + this.minPriceFilter.toString() + ","
          : "");
      filters =
        filters +
        (this.maxPriceFilter != null && this.maxPriceFilter !== ""
          ? "maxPrice:" + this.maxPriceFilter.toString() + ","
          : "");
      return filters !== "" ? filters : null;
    },
  },
  watch: {
    filters() {
      this.redirectOnFilterChange();
    },
  },
  created() {
    if (this.$route.query.search) {
      this.showFilters = true;
      this.search = this.$route.query.search;
    }
    if (this.$route.query.isbnFilter) {
      this.showFilters = true;
      this.isbnFilter = this.$route.query.isbnFilter;
    }
    if (this.$route.query.titleFilter) {
      this.showFilters = true;
      this.titleFilter = this.$route.query.titleFilter;
    }
    if (this.$route.query.categoryFilter) {
      this.showFilters = true;
      this.categoryFilter = this.$route.query.categoryFilter;
    }
    if (this.$route.query.editorialFilter) {
      this.showFilters = true;
      this.editorialFilter = this.$route.query.editorialFilter;
    }
    if (this.$route.query.authorFilter) {
      this.showFilters = true;
      this.authorFilter = this.$route.query.authorFilter;
    }
    if (this.$route.query.sourceFilter) {
      this.showFilters = true;
      this.sourceFilter = this.$route.query.sourceFilter;
    }
    if (this.$route.query.minPriceFilter) {
      this.showFilters = true;
      let value = parseFloat(this.$route.query.minPriceFilter);
      this.minPriceFilter = isNaN(value) ? null : value;
    }
    if (this.$route.query.maxPriceFilter) {
      this.showFilters = true;
      let value = parseFloat(this.$route.query.maxPriceFilter);
      this.maxPriceFilter = isNaN(value) ? null : value;
    }
    this.getItems();
  },
  methods: {
    parseBookTitle(title) {
      return lowerCaseAllWordsExceptFirstLetters(title);
    },
    updateRange([minPrice, maxPrice]) {
      this.minPriceFilter = minPrice;
      this.maxPriceFilter = maxPrice;
    },
    nextPage() {
      this.entitiesPage.page++;
      this.redirectOnTableChange();
    },
    prevPage() {
      this.entitiesPage.page--;
      this.redirectOnTableChange();
    },
    getItems() {
      this.loading = true;
      const query = this._buildQueryFromFilters();
      BookEntityRepository.getAll(query)
        .then((response) => {
          this.items = response.hits.hits.map((el) => el._source);
          this.totalItems = response.hits.total.value;
        })
        .finally(() => (this.loading = false));
    },
    redirect(query) {
      if (JSON.stringify(this.$route.query) !== JSON.stringify(query)) {
        this.$router
          .replace({
            name: "Book List",
            query: query,
          })
          .then(() => this.getItems());
      }
    },
    entityDetail(entity) {
      const selection = window.getSelection().toString();
      if (selection.length === 0) {
        this.$router.push({
          name: "Book FormDetail",
          params: { id: entity.id, backPrevious: true },
        });
      }
    },
    redirectOnTableChange(pagination = this.entitiesPage) {
      this.entitiesPage = pagination;
      let query = JSON.parse(JSON.stringify(this.$route.query));
      query.page = this.entitiesPage.page.toString();
      query.sort = generateSort(this.entitiesPage);
      this.changeQueryFilters(query);
      this.redirect(query);
    },
    changeQueryFilters(query) {
      query.search = this.search != null ? this.search : undefined;
      query.isbnFilter = this.isbnFilter != null ? this.isbnFilter : undefined;
      query.titleFilter =
        this.titleFilter != null ? this.titleFilter : undefined;
      query.categoryFilter =
        this.categoryFilter != null ? this.categoryFilter : undefined;
      query.editorialFilter =
        this.editorialFilter != null ? this.editorialFilter : undefined;
      query.authorFilter =
        this.authorFilter != null ? this.authorFilter : undefined;
      query.sourceFilter =
        this.sourceFilter != null ? this.sourceFilter : undefined;
      query.minPriceFilter =
        this.minPriceFilter != null ? this.minPriceFilter : undefined;
      query.maxPriceFilter =
        this.maxPriceFilter != null ? this.maxPriceFilter : undefined;
    },
    redirectOnFilterChange() {
      if (this.entitiesPage.page !== 1) {
        this.entitiesPage.page = 1;
      } else {
        this.redirectOnTableChange();
      }
    },
    _buildQueryFromFilters() {
      let body = bodyBuilder();
      if (this.search) {
        body.query("bool", (b) =>
          b
            .orQuery("match", "title", {
              query: this.search,
              boost: 0.75,
            })
            .orQuery("match", "author", {
              query: this.search,
              boost: 0.5,
            })
            .orQuery("match", "summary", {
              query: this.search,
              boost: 0.25,
            })
            .orQuery("match", "editorial", {
              query: this.search,
              boost: 0.5,
            })
            .orQuery("match", "category", { query: this.search, boost: 0.625 })
        );
      }
      body.query("range", "price", {
        gte: this.minPriceFilter,
        lte: this.maxPriceFilter,
      });
      if (this.titleFilter) {
        body.query("match", "title", { query: this.titleFilter, boost: 1.5 });
      }
      if (this.authorFilter) {
        body.query("match", "author", this.authorFilter);
      }
      if (this.editorialFilter) {
        body.query("match", "editorial", this.editorialFilter);
      }
      if (this.categoryFilter) {
        body.query("match", "category", {
          query: this.categoryFilter,
          boost: 1.25,
        });
      }
      if (this.isbnFilter) {
        body.filter("term", "isbn", this.isbnFilter);
      }
      if (this.sourceFilter) {
        body.filter("term", "source", this.sourceFilter);
      }
      return body
        .size(this.entitiesPage.itemsPerPage)
        .from(this.entitiesPage.itemsPerPage * (this.entitiesPage.page - 1))
        .build();
    },
  },
};
</script>
