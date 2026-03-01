package com.supplychain.finance.service;

import com.supplychain.finance.model.Invoice;
import com.supplychain.finance.repository.InvoiceRepository;
import com.supplychain.finance.service.InvoiceService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.assertThat;
import java.util.Optional;
import java.util.Arrays;
import java.util.List;

@SpringBootTest
@TestPropertySource(properties = {
    "spring.profiles.active=test"
})
public class InvoiceServiceTest {

    @Autowired
    private InvoiceService invoiceService;

    @MockBean
    private InvoiceRepository invoiceRepository;

    private Invoice testInvoice;

    @BeforeEach
    void setUp() {
        testInvoice = new Invoice();
        testInvoice.setId(1L);
        testInvoice.setAmount(1000.0);
        testInvoice.setStatus("PENDING");
    }

    @Test
    public void shouldCreateInvoice() {
        when(invoiceRepository.save(any(Invoice.class))).thenReturn(testInvoice);

        Invoice result = invoiceService.createInvoice(testInvoice);

        assertThat(result.getAmount()).isEqualTo(1000.0);
        assertThat(result.getStatus()).isEqualTo("PENDING");
        verify(invoiceRepository, times(1)).save(testInvoice);
    }

    @Test
    public void shouldGetInvoiceById() {
        when(invoiceRepository.findById(1L)).thenReturn(Optional.of(testInvoice));

        Optional<Invoice> result = invoiceService.getInvoiceById(1L);

        assertThat(result.isPresent()).isTrue();
        assertThat(result.get().getId()).isEqualTo(1L);
        verify(invoiceRepository, times(1)).findById(1L);
    }

    @Test
    public void shouldGetAllInvoices() {
        when(invoiceRepository.findAll()).thenReturn(Arrays.asList(testInvoice));

        List<Invoice> result = invoiceService.getAllInvoices();

        assertThat(result).hasSize(1);
        assertThat(result.get(0).getAmount()).isEqualTo(1000.0);
        verify(invoiceRepository, times(1)).findAll();
    }
}
