import bookListList from "./components/bookListList";

import bookFormDetail from "./components/bookFormDetail";

const routes = [
  {
    path: "/book-list",
    name: "Book List",
    component: bookListList,
    meta: {
      label: "t_book.headers.bookList",
    },
  },
  {
    path: "/book-form/:id(\\d+)",
    name: "Book FormDetail",
    component: bookFormDetail,
    meta: {
      label: "t_book.headers.bookFormDetail",
    },
  },
];

export default routes;