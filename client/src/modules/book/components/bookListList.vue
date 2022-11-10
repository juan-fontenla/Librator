<template>
  <v-container v-if="items">
    <v-card>
      <v-card-title>
        <v-row align="center" justify="space-between" no-gutters>
          <v-col class="d-none d-md-block">
            <span class="headline no-split-words">
              {{ $t($route.meta.label) }}
            </span>
          </v-col>
          <v-col
            cols="12"
            sm="7"
            md="4"
            lg="6"
            xl="8"
            order="2"
            order-sm="1"
            class="text-center text-sm-right mt-4 mt-sm-0"
          >
            <v-btn color="primary" outlined @click="showFilters = !showFilters">
              <v-icon left dark>mdi-magnify</v-icon>
              <span>
                {{ showFilters ? $t("hideFilters") : $t("showFilters") }}
              </span>
              <v-icon right dark v-if="showFilters">mdi-chevron-up</v-icon>
              <v-icon right dark v-else>mdi-chevron-down</v-icon>
            </v-btn>
          </v-col>
          <v-col order="1" order-md="2" class="text-right">
            <v-btn color="primary" @click="reportRequest()">
              <v-icon>import_export</v-icon>
              <span class="d-none d-sm-block"> {{ $t("export") }} </span>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row align="center" v-show="showFilters" justify="space-between">
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="isbnFilter"
              :label="$t('t_book.prop.isbn')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="titleFilter"
              :label="$t('t_book.prop.title')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="categoryFilter"
              :label="$t('t_book.prop.category')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="editorialFilter"
              :label="$t('t_book.prop.editorial')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="photoFilter"
              :label="$t('t_book.prop.photo')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <debounced-text-field
              dense
              v-model="authorFilter"
              :label="$t('t_book.prop.author')"
            ></debounced-text-field>
          </v-col>
          <v-col cols="12" md="2" xl="1">
            <v-select
              dense
              @change="redirectOnFilterChange"
              clearable
              :items="sourceProperty"
              :item-text="(item) => $t(item.text)"
              item-value="value"
              :menu-props="{ offsetY: true }"
              v-model="sourceFilter"
              :label="$t('t_book.prop.source')"
            >
            </v-select>
          </v-col>
          <v-col cols="6" md="2" xl="1">
            <number-field
              :debouncing="300"
              v-model="priceFilter"
              type="double"
              :label="$t('t_book.prop.price')"
            ></number-field>
          </v-col>
        </v-row>
        <v-data-table
          :headers="headers"
          :items="items"
          :options="entitiesPage"
          :server-items-length="totalItems"
          :loading="loading"
          :footer-props="tableFooterProps"
          @click:row="entityDetail"
          @update:options="redirectOnTableChange"
        >
          <template v-slot:[`item.source`]="{ item }">
            <span v-if="item.source">
              {{ $t(`source.${item.source}`) }}
            </span>
          </template>

          <template v-slot:[`item.action`]="{ item }">
            <v-icon color="primary" @click.stop="entityDetail(item)">
              description
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import DebouncedTextField from "@/components/debouncing-inputs/DebouncedTextField.vue";

import NumberField from "@/components/number-field/NumberField.vue";
import response from "@/common/mock-response";
import defaultPaginationSettings from "@/common/default-pagination-settings";
import {
  generateSort,
  parseStringToSortBy,
  parseStringToSortDesc,
} from "@/common/pagination-utils";
import tableFooterProps from "@/common/table-footer-props";

import sourceProperty from "@/enumerates/source";
import displayManyRelationship from "@/common/DisplayManyRelationships";
import reportRequestFn from "@/common/ReportRequest";
import RepositoryFactory from "@/repositories/RepositoryFactory";
const BookEntityRepository = RepositoryFactory.get("BookEntityRepository");

export default {
  name: "bookListList",
  components: {
    DebouncedTextField,
    NumberField,
  },
  data() {
    return {
      mockData: response,
      items: [],
      showFilters: false,
      sourceProperty: sourceProperty,
      isbnFilter: null,
      titleFilter: null,
      categoryFilter: null,
      editorialFilter: null,
      photoFilter: null,
      authorFilter: null,
      sourceFilter: null,
      priceFilter: null,
      entitiesPage: {
        page:
          parseInt(this.$route.query.page) || defaultPaginationSettings.page,
        itemsPerPage:
          parseInt(this.$route.query.pageSize) ||
          defaultPaginationSettings.itemsPerPage,
        sortBy: parseStringToSortBy(this.$route.query.sort),
        sortDesc: parseStringToSortDesc(this.$route.query.sort),
      },
      totalItems: 0,
      loading: false,
      tableFooterProps,
    };
  },
  computed: {
    headers() {
      return [
        {
          text: this.$t("t_book.prop.isbn"),
          value: "isbn",
        },
        {
          text: this.$t("t_book.prop.title"),
          value: "title",
        },
        {
          text: this.$t("t_book.prop.category"),
          value: "category",
        },
        {
          text: this.$t("t_book.prop.editorial"),
          value: "editorial",
        },
        {
          text: this.$t("t_book.prop.photo"),
          value: "photo",
        },
        {
          text: this.$t("t_book.prop.author"),
          value: "author",
        },
        {
          text: this.$t("t_book.prop.source"),
          value: "source",
        },
        {
          text: this.$t("t_book.prop.price"),
          value: "price",
        },
        { text: "", sortable: false, value: "action" },
      ];
    },
    filters() {
      let filters = "";
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
        (this.photoFilter != null && this.photoFilter !== ""
          ? "photo:" + this.photoFilter.toString() + ","
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
        (this.priceFilter != null && this.priceFilter !== ""
          ? "price:" + this.priceFilter.toString() + ","
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
    if (this.$route.query.photoFilter) {
      this.showFilters = true;
      this.photoFilter = this.$route.query.photoFilter;
    }
    if (this.$route.query.authorFilter) {
      this.showFilters = true;
      this.authorFilter = this.$route.query.authorFilter;
    }
    if (this.$route.query.sourceFilter) {
      this.showFilters = true;
      this.sourceFilter = this.$route.query.sourceFilter;
    }
    if (this.$route.query.priceFilter) {
      this.showFilters = true;
      let value = parseFloat(this.$route.query.priceFilter);
      this.priceFilter = isNaN(value) ? null : value;
    }
    this.getItems();
  },
  methods: {
    getItems() {
      this.loading = true;
      const options = {
        params: {
          page: this.entitiesPage.page - 1,
          filters: this.filters,
          sort: this.$route.query.sort,
          size: this.entitiesPage.itemsPerPage,
        },
      };
      BookEntityRepository.getAll(options)
        .then((response) => {
          this.items = response.content;
          this.totalItems = response.totalElements;
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
      query.pageSize = this.entitiesPage.itemsPerPage.toString();
      query.sort = generateSort(this.entitiesPage);
      this.changeQueryFilters(query);
      this.redirect(query);
    },
    changeQueryFilters(query) {
      query.isbnFilter = this.isbnFilter != null ? this.isbnFilter : undefined;
      query.titleFilter =
        this.titleFilter != null ? this.titleFilter : undefined;
      query.categoryFilter =
        this.categoryFilter != null ? this.categoryFilter : undefined;
      query.editorialFilter =
        this.editorialFilter != null ? this.editorialFilter : undefined;
      query.photoFilter =
        this.photoFilter != null ? this.photoFilter : undefined;
      query.authorFilter =
        this.authorFilter != null ? this.authorFilter : undefined;
      query.sourceFilter =
        this.sourceFilter != null ? this.sourceFilter : undefined;
      query.priceFilter =
        this.priceFilter != null ? this.priceFilter : undefined;
    },
    redirectOnFilterChange() {
      if (this.entitiesPage.page !== 1) {
        this.entitiesPage.page = 1;
      } else {
        this.redirectOnTableChange();
      }
    },
    displayManyRelationship,
    reportRequest() {
      reportRequestFn(BookEntityRepository, "Book");
    },
  },
};
</script>
