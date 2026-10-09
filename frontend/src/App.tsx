import { BrowserRouter, Route, Routes } from "react-router"
import { WorkspaceList } from "./pages/WorkspaceList"
import { Layout } from "./components/Layout"
import { MembersSettings } from "./pages/MembersSettings"
import { NoteEditor } from "./pages/NoteEditor"
import { AuthPage } from "./pages/AuthPages"
import { RegisterPage } from "./pages/RegisterPage"


function App() {

  return (
   <BrowserRouter>
  <Routes>
    <Route  element={<Layout />}>
      <Route index element={<WorkspaceList />} />
      <Route path="/notes" element={<NoteEditor role="owner" />} />
      <Route path="/members" element={<MembersSettings />} />
  </Route>
  <Route path="/auth/login" element={<AuthPage/>}/>
  <Route path="/register" element={<RegisterPage/>}/>
  </Routes>
   </BrowserRouter>
  )
}

export default App
