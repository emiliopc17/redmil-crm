import { Refine, Authenticated } from "@refinedev/core";
import { dataProvider } from "@refinedev/simple-rest";
import routerBindings, {
    CatchAllNavigate,
    NavigateToResource,
    UnsavedChangesNotifier
} from "@refinedev/react-router-v6";
import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";
import { SpotifyLayout } from "./components/Layout";
import { PDFUploadPage } from "./pages/pdf-uploads";
import { InvoiceListPage } from "./pages/invoices";
import { InvoiceCreatePage } from "./pages/invoice-create";
import { CustomerListPage } from "./pages/customers";
import { CustomerDetailsPage } from "./pages/customer-details";
import { PipelineKanbanPage } from "./pages/pipeline";
import { CRMDashboard } from "./pages/crm-dashboard";
import { LoginPage } from "./pages/login";
import { authProvider } from "./authProvider";
import "./index.css";

const App = () => {
    return (
        <BrowserRouter>
            <Refine
                dataProvider={dataProvider("http://localhost:8000/api/v1")}
                authProvider={authProvider}
                routerProvider={routerBindings}
                resources={[
                    {
                        name: "crm",
                        list: "/",
                        meta: { label: "CRM Dashboard" }
                    },
                    {
                        name: "pipeline",
                        list: "/pipeline",
                        meta: { label: "Pipeline" }
                    },
                    {
                        name: "invoices",
                        list: "/invoices",
                        meta: { label: "Facturas" }
                    },
                    {
                        name: "customers",
                        list: "/customers",
                        show: "/customers/show/:id",
                        meta: { label: "Clientes" }
                    },
                    {
                        name: "pdf-uploads",
                        list: "/pdf-uploads",
                        meta: { label: "Docling PDF" }
                    }
                ]}
                options={{
                    syncWithLocation: true,
                    warnWhenUnsavedChanges: true,
                }}
            >
                <Routes>
                    <Route
                        element={
                            <Authenticated
                                key="authenticated-inner"
                                fallback={<CatchAllNavigate to="/login" />}
                            >
                                <SpotifyLayout>
                                    <Outlet />
                                </SpotifyLayout>
                            </Authenticated>
                        }
                    >
                        <Route index element={<CRMDashboard />} />
                        <Route path="pipeline" element={<PipelineKanbanPage />} />
                        <Route path="invoices">
                            <Route index element={<InvoiceListPage />} />
                            <Route path="create" element={<InvoiceCreatePage />} />
                        </Route>
                        <Route path="customers">
                            <Route index element={<CustomerListPage />} />
                            <Route path="show/:id" element={<CustomerDetailsPage />} />
                        </Route>
                        <Route path="pdf-uploads" element={<PDFUploadPage />} />
                    </Route>
                    <Route
                        element={
                            <Authenticated key="authenticated-outer" fallback={<Outlet />}>
                                <NavigateToResource />
                            </Authenticated>
                        }
                    >
                        <Route path="/login" element={<LoginPage />} />
                    </Route>
                </Routes>
                <UnsavedChangesNotifier />
            </Refine>
        </BrowserRouter>
    );
};

export default App;
